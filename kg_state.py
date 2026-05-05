"""
kg_state.py — 流水线状态管理（SQLite）

替代用"文件是否存在"判断状态的做法，提供：
- 原子性任务领取（多进程安全）
- 精确断点续跑
- 错误记录和重试

用法:
    from kg_state import StateDB
    db = StateDB()
    db.register_files(stems)          # 初始化，把文件列表写入数据库
    stem = db.claim_one("preprocess") # 领取一个任务（原子操作）
    db.mark_done(stem, "preprocess")  # 标记完成
    db.mark_failed(stem, "preprocess", "error msg")  # 标记失败
    db.set_char_count(stem, 12345)    # 记录转换后字符数
    db.print_stats()                  # 打印进度
"""

import sqlite3
import time
from datetime import datetime
from pathlib import Path
from contextlib import contextmanager

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "kg_pipeline.db"

STAGES = ("convert", "preprocess", "extract")

# 任务超时时间（秒）：超过此时间还是 running 的任务视为卡死，重置为 pending
TASK_TIMEOUT = 600  # 10 分钟


def _now() -> str:
    """返回格式化时间字符串：月/日/年/时:分:秒"""
    return datetime.now().strftime("%m/%d/%Y/%H:%M:%S")


class StateDB:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.db_path, timeout=30)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self):
        with self._conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS papers (
                    stem              TEXT PRIMARY KEY,
                    convert_status    TEXT NOT NULL DEFAULT 'pending',
                    preprocess_status TEXT NOT NULL DEFAULT 'pending',
                    extract_status    TEXT NOT NULL DEFAULT 'pending',
                    char_count        INTEGER,
                    skip_reason       TEXT,
                    retry_count       INTEGER NOT NULL DEFAULT 0,
                    error_msg         TEXT,
                    claimed_at        REAL,
                    updated_at        TEXT
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_preprocess ON papers(preprocess_status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_extract ON papers(extract_status)")
            for col in ("char_count INTEGER", "skip_reason TEXT", "extract_model TEXT",
                        "content_hash TEXT", "convert_at TEXT",
                        "preprocess_at TEXT", "extract_at TEXT"):
                try:
                    conn.execute(f"ALTER TABLE papers ADD COLUMN {col}")
                except Exception:
                    pass
            # content_hash 唯一索引（允许 NULL）
            try:
                conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_content_hash ON papers(content_hash) WHERE content_hash IS NOT NULL")
            except Exception:
                pass

    def register_files(self, stems: list[str]):
        """把文件列表写入数据库（已存在的跳过）。"""
        with self._conn() as conn:
            conn.executemany(
                "INSERT OR IGNORE INTO papers(stem, updated_at) VALUES(?, ?)",
                [(s, _now()) for s in stems]
            )
        print(f"注册 {len(stems)} 个文件到状态库")

    def claim_one(self, stage: str) -> str | None:
        """原子性地领取一个待处理任务，返回 stem，没有任务时返回 None。

        同时把超时的 running 任务重置为 pending（处理崩溃/中断的情况）。
        """
        col = f"{stage}_status"
        now_ts = time.time()

        with self._conn() as conn:
            # 先重置超时任务
            conn.execute(f"""
                UPDATE papers SET {col}='pending', claimed_at=NULL, updated_at=?
                WHERE {col}='running' AND claimed_at < ?
            """, (_now(), now_ts - TASK_TIMEOUT))

            # 原子领取一个 pending 任务（跳过已标记 skip 的）
            # extract 阶段额外要求 preprocess 已完成
            extra = "AND preprocess_status='done'" if stage == "extract" else ""
            row = conn.execute(f"""
                SELECT stem FROM papers
                WHERE {col}='pending' AND skip_reason IS NULL {extra}
                LIMIT 1
            """).fetchone()

            if not row:
                return None

            stem = row["stem"]
            conn.execute(f"""
                UPDATE papers SET {col}='running', claimed_at=?, updated_at=?
                WHERE stem=?
            """, (now_ts, _now(), stem))

        return stem

    def mark_done(self, stem: str, stage: str):
        col = f"{stage}_status"
        at_col = f"{stage}_at"
        with self._conn() as conn:
            conn.execute(f"""
                UPDATE papers SET {col}='done', {at_col}=?, error_msg=NULL, updated_at=?
                WHERE stem=?
            """, (_now(), _now(), stem))

    def mark_failed(self, stem: str, stage: str, error_msg: str):
        col = f"{stage}_status"
        with self._conn() as conn:
            conn.execute(f"""
                UPDATE papers
                SET {col}='failed',
                    retry_count=retry_count+1,
                    error_msg=?,
                    updated_at=?
                WHERE stem=?
            """, (str(error_msg)[:500], _now(), stem))

    def set_char_count(self, stem: str, char_count: int):
        """记录 convert 后的 MD 字符数。"""
        with self._conn() as conn:
            conn.execute(
                "UPDATE papers SET char_count=?, updated_at=? WHERE stem=?",
                (char_count, _now(), stem)
            )

    def skip(self, stem: str, reason: str):
        """标记文件为跳过（字符数不足、非论文等），所有阶段均设为 skipped。"""
        with self._conn() as conn:
            conn.execute("""
                UPDATE papers
                SET skip_reason=?,
                    preprocess_status='skipped',
                    extract_status='skipped',
                    updated_at=?
                WHERE stem=?
            """, (reason[:200], _now(), stem))

    def check_and_set_hash(self, stem: str, content_hash: str) -> str | None:
        """尝试写入 content_hash。
        若哈希已存在（重复文件），返回已有文件的 stem；否则写入并返回 None。
        线程安全：并发冲突时通过捕获唯一约束异常处理。
        """
        with self._conn() as conn:
            existing = conn.execute(
                "SELECT stem FROM papers WHERE content_hash=?", (content_hash,)
            ).fetchone()
            if existing:
                return existing["stem"]
            try:
                conn.execute(
                    "UPDATE papers SET content_hash=?, updated_at=? WHERE stem=?",
                    (content_hash, _now(), stem)
                )
            except Exception:
                # 并发冲突：另一个线程刚写入了相同哈希，查出它是谁
                row = conn.execute(
                    "SELECT stem FROM papers WHERE content_hash=?", (content_hash,)
                ).fetchone()
                return row["stem"] if row else None
        return None

    def set_extract_model(self, stem: str, model: str):
        """记录 extract 阶段使用的模型。"""
        with self._conn() as conn:
            conn.execute(
                "UPDATE papers SET extract_model=?, updated_at=? WHERE stem=?",
                (model, _now(), stem)
            )

    def release(self, stem: str, stage: str):
        """把任务放回 pending（用于不属于本次批次的文件）。"""
        col = f"{stage}_status"
        with self._conn() as conn:
            conn.execute(f"""
                UPDATE papers SET {col}='pending', claimed_at=NULL, updated_at=?
                WHERE stem=?
            """, (_now(), stem))

    def reset_failed(self, stage: str):
        """把某阶段所有 failed 重置为 pending，用于重跑失败任务。"""
        col = f"{stage}_status"
        with self._conn() as conn:
            n = conn.execute(f"""
                UPDATE papers SET {col}='pending', updated_at=?
                WHERE {col}='failed'
            """, (_now(),)).rowcount
        print(f"重置 {n} 个 {stage} 失败任务")

    def get_stats(self) -> dict:
        with self._conn() as conn:
            rows = conn.execute("""
                SELECT
                    COALESCE(SUM(convert_status='done'), 0)    as conv_done,
                    COALESCE(SUM(convert_status='pending'), 0) as conv_pending,
                    COALESCE(SUM(convert_status='failed'), 0)  as conv_fail,
                    COALESCE(SUM(preprocess_status='done'), 0)    as pre_done,
                    COALESCE(SUM(preprocess_status='pending'), 0) as pre_pending,
                    COALESCE(SUM(preprocess_status='failed'), 0)  as pre_fail,
                    COALESCE(SUM(extract_status='done'), 0)    as ext_done,
                    COALESCE(SUM(extract_status='pending'), 0) as ext_pending,
                    COALESCE(SUM(extract_status='failed'), 0)  as ext_fail,
                    COALESCE(SUM(skip_reason IS NOT NULL), 0)  as skipped,
                    COUNT(*) as total
                FROM papers
            """).fetchone()
            return dict(rows)

    def print_stats(self):
        s = self.get_stats()
        total = s["total"]
        with self._conn() as conn:
            row = conn.execute("""
                SELECT COUNT(char_count) as with_chars,
                       SUM(char_count) as total_chars,
                       AVG(char_count) as avg_chars
                FROM papers WHERE char_count IS NOT NULL
            """).fetchone()
        print(f"\n{'='*50}")
        print(f"总计: {total} 篇  (已跳过: {s['skipped']})")
        print(f"  convert:    done={s['conv_done']}  pending={s['conv_pending']}  failed={s['conv_fail']}")
        print(f"  preprocess: done={s['pre_done']}  pending={s['pre_pending']}  failed={s['pre_fail']}")
        print(f"  extract:    done={s['ext_done']}  pending={s['ext_pending']}  failed={s['ext_fail']}")
        if row and row["with_chars"]:
            total_chars = row["total_chars"] or 0
            avg_chars = row["avg_chars"] or 0
            print(f"  字符统计:   已记录={row['with_chars']}篇  总字符={total_chars:,}  平均={avg_chars:,.0f}")
        print(f"{'='*50}\n")


if __name__ == "__main__":
    db = StateDB()
    db.print_stats()
