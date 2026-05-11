# SciDB 10 Datasets — 知识抽取结果

## 概况

| 项目 | 数值 |
|------|------|
| 数据集 | 10 个 (ChinaUIS, DroneRFa, FRB, FRB20220912a, Fish Iridovirus, PeriCBD, Pinglu Canal, SSP1-5, Single season rice) |
| 论文总数 | 156 篇 |
| 抽取成功 | 141 篇 |
| convert 失败 | 4 篇（PDF 文件损坏或为空） |
| 内容重复跳过 | 7 篇（与已处理论文 MD5 一致） |
| 知识条目总计 | 7,322 条 |
| 平均每篇 | 51.9 条 |

## 抽取方法

| 组 | 类型 | 描述 |
|----|------|------|
| G1 | concept, relation | 概念与关系 |
| G2 | dataset, data_specification | 数据集与数据规范 |
| G3 | method, experiment | 方法与实验 |
| G4 | quantitative_result, performance_result | 量化结果与性能对比 |
| G5 | claim, conclusion, limitation, future_work | 主张、结论、局限与展望 |

## 各类型统计

| 知识类型 | 总数 | 均/篇 | evidence 中位数(字符) |
|---------|------|--------|---------------------|
| concept | 1,323 | 9.4 | 986 |
| relation | 975 | 6.9 | 902 |
| dataset | 515 | 3.7 | 1,075 |
| method | 721 | 5.1 | 991 |
| experiment | 517 | 3.7 | 1,170 |
| quantitative_result | 1,233 | 8.7 | 449 |
| performance_result | 523 | 3.7 | 582 |
| data_specification | 589 | 4.2 | 856 |
| claim | 271 | 1.9 | 1,359 |
| conclusion | 221 | 1.6 | 1,141 |
| limitation | 242 | 1.7 | 1,029 |
| future_work | 192 | 1.4 | 762 |

## 目录结构

```
scidb_output/
  ChinaUIS Dataset/          (9 篇)
  DroneRFa/                  (12 篇)
  FRB20220912a/              (15 篇)
  Fast Radio Bursts/         (21 篇)
  Fish Iridovirus/           (28 篇)
  PeriCBD/                   (13 篇)
  Pinglu Canal/              (11 篇)
  SSP1-5/                    (16 篇)
  Single_season_rice/        (16 篇)
```

## 失败文件说明

### convert 失败（PDF 文件损坏或为空，无法解析）

| 文件 | 原因 |
|------|------|
| ChinaUIS: Urban informal settlements interpretation... | PDF 文件为空（0 字节） |
| Fast Radio Bursts: 03_Ninety_percent_circular_polarization... | PDF 解析返回 null |
| Fast Radio Bursts: 05_Understanding_radio_polarimetry_III... | PDF 解析返回 null |
| Single_season_rice: Canopy structure dynamics constraints... | PDF 文件为空（0 字节） |

### 内容重复跳过（MD5 哈希与已处理论文完全一致）

| 跳过文件 | 与以下文件内容重复 |
|---------|------------------|
| Fast Radio Bursts: 21_Highly_magnetized_environment... | 06_Extreme_Magneto_ionic_Environment_FRB_121102 |
| FRB20220912a: 22_FAST_observations_FRB_20220912A... | 03_FAST_Observations_of_FRB_20220912A_Burst_Properties_and_Polarization |
| Fast Radio Bursts: 23_FAST_observations_active_episode... | 04_FAST_Observations_FRB_20201124A_Burst_Morphology |
| FRB20220912a: 24_Investigating_FRB_20240114A_FAST... | 07_Investigating_FRB_20240114A_with_FAST_Morphological_Classification |
| Fast Radio Bursts: 26_CHIME_FRB_catalog_1 | 11_CHIME_FRB_Catalog_1 |
| FRB20220912a: 28b_Persistently_active_FRB_embedded... | 28_Persistently_active_FRB_embedded_in_expanding_SNR |
| SSP1-5: Projecting 1 km-grid population distributions... | 10b_Projecting_1km_grid_population_2020_2100_under_SSPs |
