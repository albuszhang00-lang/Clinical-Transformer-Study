# 第 5–9 周执行计划：复现 Clinical Transformer

> 周期：5 周 × 20 小时 = 100 小时  
> 数据：Chowell 2021（公开，train 1184 / test 295）  
> 目标：复现论文的表格 Clinical Transformer，完成一个可复核的最小结果  
> 已有基线：Week 2 RF AUROC 0.8055；Week 3 OS C-index 0.7331、PFS C-index 0.6826

---

## 0. 先明确“复现”的边界

1. 论文的 Clinical Transformer 是**表格 `[Key, Value]` Transformer**，不是 ClinicalBERT 那类文本模型。
2. 论文用了多个队列；我们只做 **Chowell 2021**。
3. 论文用 **10 个 train/test split**，我们只有一个固定 split。**不要追求精确复现论文数字**，追求架构、流程和趋势。
4. 两条线：
   - **最低目标（必须完成）**：实现架构 → 从零训练 → Response AUROC + OS C-index → 与 Week 2/3 基线对比 → 一张图/表。
   - **进阶目标（时间允许）**：预训练增益、PFS、3 个随机种子、注意力/特征重要性、尝试迁移学习。
5. **不做**：完整复刻论文所有数据集、从零预训练大规模 TCGA、irAE、自有直肠癌数据（第 10 周以后）。

---

## 1. 五周总览

| 周 | 重点 | 核心交付 | 组会 |
|---|---|---|---|
| 5 | 读论文、读代码、定目标 | `docs/paper_notes.md`、`docs/reproduction_target.md` | 架构 + 目标 |
| 6 | 实现核心模型 | `dataset.py`、`model.py`、smoke test | 架构 + shape |
| 7 | 预训练 + 微调 | 预训练曲线、微调结果 | 预训练 + 微调 |
| 8 | 实验 + 消融 | 对比表、消融表、图 | 5 页结果 |
| 9 | 汇总 + 报告 | 最终表、报告、干净仓库 | 5 页总结 |

---

## 2. 第 5 周：读论文、读代码、定目标

### 学习目标

- 理解 `[Key, Value]` 输入、feature-name embedding、value embedding、无位置编码、`[TASK]`、`[MASK]`。
- 理解预训练（masked feature-name prediction）与微调（生存/分类）。
- 理解 Chowell 队列在论文中的角色：survival modeling + transfer learning。

### 任务

- [ ] 精读论文：Introduction、Results（Chowell 部分）、Methods、Supplementary。
- [ ] 写 `docs/paper_notes.md`，回答 10 个问题：
  1. 输入是什么？序列长度是多少？
  2. Key 和 Value 分别怎么 embedding？
  3. 为什么没有位置编码？
  4. 预训练任务是什么？mask 什么？预测什么？
  5. 微调任务是什么？损失函数是什么？
  6. `[TASK]` token 怎么用？
  7. 论文用了哪些数据集？Chowell 的角色是什么？
  8. 评价指标是什么？C-index 还是 AUROC？
  9. 代码在哪里？能否运行？
  10. 哪些结果是我们可以复现的？
- [ ] 检查 Code Ocean capsule 是否可访问，记录：能否打开、能否运行、是否包含预训练权重。
- [ ] 读 Chowell 原代码（GitHub）理解 17 个特征和 RF16 基线；注意它不是 Clinical Transformer。
- [ ] 写 `docs/reproduction_target.md`（1 页）：
  - 主指标：**OS C-index**（Chowell test）
  - 副指标：**Response AUROC**
  - 可选：pretraining gain
  - 复现的图/表：论文 Fig 2 或 Table 2 中 Chowell 相关结果（如果可读）
  - 允许差距：±0.05，并解释原因
- [ ] 建代码骨架：

```text
src/clinical_transformer/
├── __init__.py
├── dataset.py
├── model.py
├── pretrain.py
├── finetune.py
├── evaluate.py
└── utils.py
configs/chowell_ct.yaml
tests/
notebooks/week05/
```

### 交付

- `docs/paper_notes.md`
- `docs/reproduction_target.md`
- 代码骨架
- 3 页组会：架构图 + 复现目标 + 风险

### 验收

- 能在 5 分钟内讲清模型，不看论文。
- 能画出数据流：原始表格 → `[Key, Value]` tokens → embeddings → Transformer → `[TASK]` → 预测。
- 明确知道第 9 周要复现哪个数字/图。

### 风险与兜底

- Code Ocean 打不开 → 按论文方法自己实现；用 RF 基线做 sanity check。
- 论文方法描述不清 → 写下假设，做小实验验证，并在报告中说明。

---

## 3. 第 6 周：实现核心模型

### 学习目标

- `nn.Embedding`、`nn.TransformerEncoderLayer`、`batch_first`、attention mask、`[TASK]`/`[MASK]`。
- 理解“每个特征是一个 token”，而不是把 17 个特征拼成一个向量。

### 任务

- [ ] `dataset.py`：
  - 每个患者 → **17 个 feature tokens + 1 个 `[TASK]`**。
  - 每个 token：`key_id`（0–16）、`value`（标量）、可选类别。
  - 数值特征做标准化；类别特征（癌种）用 embedding 或 one-hot。
  - 返回 `input_ids`、`values`、`labels`、`time`、`event`。
- [ ] `model.py`：
  - key embedding：`nn.Embedding(n_features, d_model)`。
  - value embedding：共享 `nn.Linear(1, d_model)`，或每个特征一个线性层。
  - token = key_embedding + value_embedding。
  - `[TASK]` token：一个可学习的 embedding，放在序列前面。
  - Transformer encoder：2–4 层、4 heads、`d_model=64–128`、FFN 256、dropout 0.1–0.2，**不加位置编码**。
  - 输出头：分类（BCEWithLogits）或生存（风险分数）。
- [ ] 单元测试：
  - 输入 shape：`(B, 18, d_model)`。
  - `[TASK]` 输出 shape：`(B, d_model)`。
  - masking：把 key 替换成 `[MASK]` id，label 是被 mask 的 feature id。
  - backward：梯度存在且不是 NaN。
- [ ] Smoke test：在 32 个样本上过拟合，AUROC > 0.9；如果做不到，先调试模型/数据。
- [ ] 实现“从零训练”脚本（无预训练）。

### 交付

- `dataset.py`、`model.py`、`tests/`
- `notebooks/week06/w06_model_smoke_test.ipynb`
- 3 页组会：架构 + shape + smoke test

### 验收

- CPU 能跑；loss 下降；tiny subset 能过拟合；无数据泄漏。
- 预处理器只在训练集 fit。

### 风险与兜底

- shape 错误 → 每一步打印 shape；先用 `B=4` 的假数据。
- 模型不学习 → 检查 label、损失、学习率、数据标准化；先过拟合 32 个样本。
- 过拟合 → 小模型、dropout、weight decay、early stopping。

---

## 4. 第 7 周：预训练 + 微调

### 学习目标

- Masked feature-name prediction；预训练循环；微调；gradual learning vs transfer learning。

### 任务

- [ ] `pretrain.py`：
  - 随机 mask **15–30%** 的 feature keys（把 key 替换成 `[MASK]` id）。
  - 模型预测被 mask 的 feature id（17 类交叉熵）。
  - 记录 masked accuracy 和 loss。
  - 测试两种 masking：只 mask key vs mask key+value；记录差异。
- [ ] `finetune.py`：
  - 加载预训练 encoder（或随机初始化）。
  - `[TASK]` 输出 → 线性头。
  - Response：`BCEWithLogitsLoss` + `pos_weight`。
  - OS/PFS：Cox partial likelihood（先用 synthetic data 测试；再和 `lifelines` Cox 对比方向）。
  - AdamW，lr 1e-4/1e-3，weight decay 1e-4，batch 64，early stopping。
- [ ] 三个实验：
  1. **from scratch**（无预训练）
  2. **pretrain on Chowell train → fine-tune**（gradual learning）
  3. 可选：**pretrain on TCGA subset → fine-tune**（transfer learning；特征对齐难，时间不够就跳过）
- [ ] 日志：train/val loss、val AUROC/C-index、best epoch、test metric。

### 交付

- `pretrain.py`、`finetune.py`、`configs/`
- `results/w07_pretrain_curve.png`
- `results/w07_finetune_results.csv`
- 3 页组会：预训练 loss + 微调结果

### 验收

- 预训练 loss 下降。
- 微调至少不差于随机初始化；如果更差，记录并解释。
- test 只评估一次；validation 用于早停。

### 风险与兜底

- 1184 个样本预训练可能没有增益 → 如实报告；预训练增益是进阶目标，不是必须。
- Cox loss 实现错误 → 先用 Response 分类跑通；再用 synthetic data 单元测试 Cox loss。
- 预训练不稳定 → 降低 mask 比例、减小模型、增加 warmup。

---

## 5. 第 8 周：实验 + 消融

### 任务

- [ ] 跑 **3 个随机种子**：42、123、2024。
- [ ] 模型：
  - Logistic / RandomForest（复用 Week 2）
  - MLP（复用 Week 4）
  - Clinical Transformer from scratch
  - Clinical Transformer pretrained（gradual）
- [ ] 终点：
  - Response：AUROC、AUPRC、校准
  - OS/PFS：C-index
- [ ] 消融：
  - with / without value embedding
  - with / without feature-name embedding（value-only）
  - with / without pretraining
  - Transformer vs MLP
- [ ] 统计：mean ± SD、95% CI；保存：
  - `results/w08_ct_comparison.csv`
  - `results/w08_ablation.csv`
- [ ] 误差分析：按癌种分层、校准曲线、假阳性/假阴性。
- [ ] 可解释性（可选）：attention weights 或 permutation importance；和 TMB、MSI、NLR、白蛋白等已知标志物对照。

### 交付

- 两个结果 CSV
- 图：带误差棒的柱状图、校准曲线、attention heatmap（可选）
- 5 页组会

### 验收

- 至少一个 CT 配置与 MLP/Logistic 可比；如果不如，解释原因。
- 每个数字都能对上：model / pretraining / endpoint / seed / split / metric。

### 风险与兜底

- 时间不够 → 优先 Response AUROC + OS C-index；砍掉 PFS、attention、TCGA 迁移。
- 小数据导致 CI 很宽 → 报告 CI，不只看点估计。
- CT 不如 RF → 这是可能且诚实的结果；论文的增益主要来自预训练和更大数据。

---

## 6. 第 9 周：汇总 + 报告

### 任务

- [ ] 复现一张论文图/表（或明确记录为什么不能复现）。
- [ ] 最终表：baselines vs CT；mean ± SD；test metrics；CI。
- [ ] 写 5–10 页报告：背景、方法、数据、结果、消融、局限、下一步。
- [ ] 清理代码：README、config、可复现命令、tests。
- [ ] 准备第 10 周：公开直肠癌代理数据、数据字典、终点、SAP。
- [ ] 5 页组会。

### 交付

- `docs/week5-9_report.md`
- `results/w09_final_table.csv`
- `results/w09_*.png`
- 干净仓库 + README
- 5 页组会

### 验收

- 新人按 README 在 1 小时内能复现主结果。
- 所有结论都能追溯到表/图。
- 局限性写清楚：单次 split、小样本、无外部验证、预训练规模有限。

---

## 7. 每周节奏（20 小时）

| 时间 | 安排 |
|---|---|
| 周一 | 写下本周 1 个可验收目标（一个数字/一张图） |
| 周二–周四 | 写代码/跑实验；卡住超过 2 小时就记录报错并求助 |
| 周五 | 更新 `results/` 和 `docs/progress.md`；重启并运行全部 notebook |
| 周六 | 3 页组会 + commit + push |

时间分配建议：

- 4 小时：读论文/教程/源码
- 14 小时：写代码/跑实验
- 2 小时：记录、画图、准备组会

---

## 8. 建议的代码结构

```text
clinical-transformer-learning/
├── configs/
│   └── chowell_ct.yaml
├── src/clinical_transformer/
│   ├── __init__.py
│   ├── dataset.py
│   ├── model.py
│   ├── pretrain.py
│   ├── finetune.py
│   ├── evaluate.py
│   └── utils.py
├── tests/
│   ├── test_dataset.py
│   ├── test_model.py
│   └── test_loss.py
├── notebooks/
│   ├── week05/
│   ├── week06/
│   ├── week07/
│   ├── week08/
│   └── week09/
└── results/
```

---

## 9. 关键技术决定

| 项目 | 决定 |
|---|---|
| 序列长度 | 17 个 feature tokens + 1 个 `[TASK]` = 18 |
| Key embedding | `nn.Embedding(n_features, d_model)` |
| Value embedding | 共享 `nn.Linear(1, d_model)` 或每个特征一个线性层 |
| 类别特征 | 癌种用 embedding 或 one-hot；其余二值特征按数值处理 |
| 位置编码 | **不加**（按论文） |
| Transformer | 2–4 层、4 heads、`d_model=64–128`、FFN 256、dropout 0.1–0.2 |
| 预训练 | mask 15–30% feature keys，预测 feature id |
| 微调（分类） | `[TASK]` → 线性头 → BCEWithLogits |
| 微调（生存） | `[TASK]` → 风险分数 → Cox partial likelihood |
| 评价 | Response：AUROC/AUPRC/校准；生存：C-index |
| 重复 | 3 个 seed；报告 mean ± SD |
| 测试集 | 只在最终评估用一次 |

---

## 10. 最低目标 vs 进阶目标

| 级别 | 内容 | 是否必须 |
|---|---|---|
| 最低 | 实现架构；从零训练；Response AUROC；OS C-index；与基线对比；一张图/表 | ✅ 必须 |
| 进阶 | 预训练增益；PFS；3 seeds；注意力/特征重要性 | ⏳ 尽量 |
| 额外 | TCGA 迁移学习；5-fold CV；外部验证 | ❌ 时间允许再说 |

---

## 11. 风险与兜底

| 风险 | 可能性 | 影响 | 兜底 |
|---|---|---|---|
| Code Ocean 打不开 | 中 | 高 | 按论文实现；用 GitHub RF 代码辅助理解特征 |
| 预训练没有增益 | 高 | 中 | 如实报告；from-scratch 结果也是结果 |
| CT 不如 RF/MLP | 高 | 中 | 解释原因：小数据、单次 split、预训练不充分 |
| Cox loss 实现错误 | 中 | 高 | 先用 Response 分类；synthetic data 单元测试 |
| GPU 未开通 | 中 | 低 | 小模型 CPU 可跑；GPU 只用于多 seed/大模型 |
| 时间超支 | 高 | 高 | 保最低目标；砍掉 PFS/attention/TCGA |
| 过拟合 | 高 | 中 | 小模型、dropout、weight decay、early stopping、报告 CI |

---

## 12. 第 9 周验收清单

- [ ] 代码能从 README 一条命令跑通
- [ ] `results/w08_ct_comparison.csv` 包含 baselines vs CT
- [ ] `results/w09_final_table.csv` 包含 mean ± SD / CI
- [ ] 至少一张复现的图/表，或明确的“无法复现”说明
- [ ] `docs/week5-9_report.md` 5–10 页
- [ ] 5 页组会
- [ ] 第 10 周公开直肠癌代理数据计划

---

## 13. 参考资料

- Clinical Transformer 论文：  
  https://www.nature.com/articles/s41467-025-57181-2
- 论文代码（Code Ocean）：  
  https://doi.org/10.24433/co.6684503.v2
- Chowell 数据集（Hugging Face）：  
  https://huggingface.co/datasets/gabrielaltay/chowell-2021
- Chowell 原论文：  
  https://doi.org/10.1038/s41587-021-01070-8
- Chowell 原代码（RF16 基线，不是 Clinical Transformer）：  
  https://github.com/CCF-ChanLab/MSK-IMPACT-IO
- 论文 Fig 1（架构）：  
  https://www.nature.com/articles/s41467-025-57181-2/figures/1
- 论文 Table 1（数据集）：  
  https://www.nature.com/articles/s41467-025-57181-2/tables/1
