"""
stats_output.py — 统计 scidb_output 中 JSON 的结构信息
每篇论文：每种知识类型数量 + evidence 长度
"""
import json
import sys
from pathlib import Path
from collections import defaultdict

SCIDB = Path(__file__).parent / "scidb_output"


def stats_one(json_path: Path) -> dict:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    tc = defaultdict(int)
    ev_lens = defaultdict(list)
    for e in entries:
        t = e["type"]
        tc[t] += 1
        ev = e.get("evidence", {})
        ot = ev.get("original_text", "")
        ev_lens[t].append(len(ot))
    return {"total": len(entries), "counts": dict(tc), "ev_lens": {t: sorted(v) for t, v in ev_lens.items()}}


def main():
    results = {}
    global_tc = defaultdict(int)
    global_ev = defaultdict(list)

    for folder in sorted(SCIDB.iterdir()):
        if not folder.is_dir():
            continue
        for jf in sorted(folder.glob("*.json")):
            key = f"{folder.name}/{jf.stem}"
            try:
                r = stats_one(jf)
                results[key] = r
                for t, c in r["counts"].items():
                    global_tc[t] += c
                    global_ev[t].extend(r["ev_lens"][t])
            except Exception as e:
                print(f"  ✗ {key}: {e}")

    n_papers = len(results)
    n_entries = sum(r["total"] for r in results.values())
    print(f"┌{'─'*58}┐")
    print(f"│  scidb_output 结构统计: {n_papers} 篇论文, {n_entries} 条知识        │")
    print(f"├{'─'*22}┬{'─'*10}┬{'─'*12}┬{'─'*12}┤")
    print(f"│ {'知识类型':<20} │ {'总数':>8} │ {'均/篇':>10} │ {'evidence均长':>10} │")
    print(f"├{'─'*22}┼{'─'*10}┼{'─'*12}┼{'─'*12}┤")

    type_order = ["concept", "relation", "dataset", "method", "experiment",
                  "quantitative_result", "performance_result", "data_specification",
                  "claim", "conclusion", "limitation", "future_work"]

    n_expected = 0
    for t in type_order:
        c = global_tc.get(t, 0)
        avg_per = round(c / n_papers, 1) if n_papers else 0
        lens = global_ev.get(t, [])
        avg_len = round(sum(lens) / len(lens)) if lens else 0
        print(f"│ {t:<20} │ {c:>8} │ {avg_per:>10} │ {avg_len:>10} │")
        n_expected += 1

    print(f"├{'─'*22}┴{'─'*10}┴{'─'*12}┴{'─'*12}┤")
    total_c = sum(global_tc.values())
    total_avg = round(total_c / n_papers, 1) if n_papers else 0
    all_lens = [v for lst in global_ev.values() for v in lst]
    all_avg_len = round(sum(all_lens) / len(all_lens)) if all_lens else 0
    print(f"│ {'合计':<20} │ {total_c:>8} │ {total_avg:>10} │ {all_avg_len:>10} │")
    print(f"└{'─'*22}┴{'─'*10}┴{'─'*12}┴{'─'*12}┘")

    # evidence 长度分布
    print(f"\n┌{'─'*40}┐")
    print(f"│ evidence 长度分布 (字符数)                │")
    print(f"├{'─'*8}┬{'─'*8}┬{'─'*8}┬{'─'*8}┬{'─'*8}┤")
    print(f"│ {'类型':<6} │ {'p25':>6} │ {'p50':>6} │ {'p75':>6} │ {'max':>6} │")
    print(f"├{'─'*8}┼{'─'*8}┼{'─'*8}┼{'─'*8}┼{'─'*8}┤")
    for t in type_order:
        lens = sorted(global_ev.get(t, []))
        if not lens:
            continue
        n = len(lens)
        p25 = lens[int(n * 0.25)]
        p50 = lens[int(n * 0.50)]
        p75 = lens[int(n * 0.75)]
        pmax = lens[-1]
        print(f"│ {t:<6} │ {p25:>6} │ {p50:>6} │ {p75:>6} │ {pmax:>6} │")
    print(f"└{'─'*8}┴{'─'*8}┴{'─'*8}┴{'─'*8}┴{'─'*8}┘")


if __name__ == "__main__":
    main()
