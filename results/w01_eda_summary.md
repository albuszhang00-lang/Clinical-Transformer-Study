# Week 1 EDA 摘要

## 数据规模

- train：__1184_ 行 × __28_ 列
- test：_295__ 行 × _28__ 列

## 结局分布

- Response 比例：_26.9__%（分母 _1184__）
- OS 事件数：_701__
- PFS 事件数：_991__

## 缺失情况

缺失最多的 3 列：

数据无缺失

## 癌种分布

- 样本量最大的 3 个癌种：_NSCLC__、_Melanoma__、_Renal__
- 响应率最高：_Melanoma__
- 响应率最低：_Pancreatic__

## 图

- `results/w01_age_hist.png`
- `results/w01_nlr_boxplot.png`

## 结论

- 
- 
- 

## 局限

- 单次固定 train/test 划分，不能代表论文的 10 次划分。
- 泛癌种数据，不是直肠癌。
- 未做缺失值插补；缺失机制未知。
