# 第 0–4 周执行清单

> 每周 20 小时。原则：**每周必须有一个能跑的 notebook 和一个数字**；不以“看完课程”为完成标准。

---

## 第 0 周（10 小时）：环境与数据

### 目标

能把项目跑起来，并且知道每一步在干什么。

### 任务

- [ ] 安装 Miniconda、VS Code、Git；注册 GitHub。
- [ ] 创建 conda 环境：`conda env create -f environment.yml`。
- [ ] 激活环境：`conda activate ctlearn`。
- [ ] 运行 `python src/check_env.py`，确认所有包 OK。
- [ ] 运行 `python src/load_chowell.py`，确认 `data/raw/chowell_train.csv` 和 `chowell_test.csv` 生成。
- [ ] 用 VS Code 打开项目，选择 `ctlearn` 内核。
- [ ] 测试 SSH 连医院服务器，运行 `nvidia-smi`，截图/保存输出。
- [ ] `git init` + 第一次 commit + push。

### 验收

- `check_env.py` 输出所有包版本，`CUDA available` 显示 True/False 均可。
- Chowell 数据 shape 为 **train 1.18k / test 295**（以实际下载为准），17 个特征列存在。
- 能在本地打开 CSV，看到 `Response`、`OS_Event`、`PFS_Event` 三列。
- 仓库有 README、environment.yml、src、data、notebooks 目录。

### 周会 3 页

1. 环境截图（Python 版本 + 包列表）。
2. Chowell 数据 shape、缺失率前 5、Response 分布。
3. 卡点（例如 conda 激活、HF 下载、SSH）。

### 注意

- **不要**用 `RF16_prob` 当特征：它是别人模型输出的概率，会造成泄漏。
- `SAMPLE_ID` 是 ID，不是特征。
- 第 0 周不要求看懂论文。

---

## 第 1 周（20 小时）：Python 基础 + pandas

### 学习目标

- 能读写 Python 脚本，理解变量、列表、字典、循环、函数、文件读写、异常。
- 能用 pandas 做：读取、筛选、分组、缺失统计、简单绘图。

### 建议节奏

| 天 | 内容 | 小时 |
|---|---|---|
| 1 | Python 语法：变量/类型/列表/字典/条件/循环 | 4 |
| 2 | 函数/模块/文件读写/异常；写 10 个小练习 | 4 |
| 3 | pandas：`read_csv`、`head/info/describe`、`loc/iloc`、布尔索引 | 4 |
| 4 | pandas：`groupby`、`value_counts`、`isna`、`sort_values`、`merge` | 4 |
| 5 | 在 Chowell 上做 EDA，整理 notebook + 周会 | 4 |

### 练习（必须动手）

1. 写一个函数 `summarize(df, col)`，返回该列的 count、mean、median、缺失数。
2. 用 pandas 读出 `chowell_train.csv`，打印 shape、列名、每列缺失率。
3. 统计 `Response` 的分布，计算 responder 比例。
4. 按 `Cancer_Type` 分组，计算每组的样本量和 responder 比例。
5. 画两张图：Age 直方图；按 Response 分组的 NLR 箱线图。
6. 找出 NLR 最高和最低的 5 个样本（只显示 ID + NLR + Response）。

### 交付

- `notebooks/w01_eda.ipynb`
- 一张缺失率表 + 两张图
- 周会 3 页

### 自测

不看笔记，写出：读取 CSV、筛选 `Response == 1`、按 `Cancer_Type` 求均值、统计缺失率。

---

## 第 2 周（20 小时）：预处理 + sklearn 基线

### 学习目标

- 理解训练/测试划分、缺失值处理、类别编码、标准化。
- 能训练 logistic regression、random forest、XGBoost，并正确评价。

### 任务

- [ ] 用 `ColumnTransformer` + `Pipeline` 搭建预处理：
  - 数值：中位数填补 + 标准化；
  - 类别：众数填补 + OneHotEncoder（或直接使用已编码的 `Cancer_Type2`）。
- [ ] 训练三个基线：
  - LogisticRegression
  - RandomForestClassifier
  - XGBoost（或 HistGradientBoostingClassifier）
- [ ] 在 **训练集** 做 5 折交叉验证，在 **测试集** 只评估一次。
- [ ] 指标：AUROC、AUPRC、准确率、混淆矩阵、校准曲线。
- [ ] 用 bootstrap 给测试集 AUROC 一个 95% 置信区间。
- [ ] 把结果写入 `results/baseline_metrics.csv`。

### 数据列提示

- 目标：`Response (1:Responder; 0:Non-responder)`
- 排除：`SAMPLE_ID`、`RF16_prob`、`Cancer_type_grouped_2`、`Cancer_Type`（字符串）、`Drug_class`、`Stage at IO start`（字符串）。
- 特征：17 列，见 `src/load_chowell.py` 里的 `FEATURES`。

### 交付

- `notebooks/w02_baselines.ipynb`
- `results/baseline_metrics.csv`
- 一张校准曲线图 + 一张 ROC 曲线图

### 铁律

- **测试集只能用一次。** 不要根据测试集结果回头调参。
- 所有预处理必须放进 Pipeline，防止泄漏。
- 每个数字都要注明：哪个模型、哪个数据划分、哪个指标。

---

## 第 3 周（20 小时）：生存分析

### 学习目标

- 理解删失（censoring）、Kaplan–Meier、log-rank、Cox 比例风险、C-index。
- 能在 Chowell 上做 OS/PFS 基线。

### 任务

- [ ] 用 `lifelines` 画 OS 和 PFS 的 Kaplan–Meier 曲线。
- [ ] 按 Response 分组做 log-rank 检验。
- [ ] 用 CoxPHFitter 拟合临床特征（Age、Sex、Stage、NLR、Albumin、TMB 等）。
- [ ] 计算训练集/测试集 C-index。
- [ ] 检查比例风险假设（`check_assumptions`，可选）。
- [ ] 把结果写入 `results/survival_metrics.csv`。

### 注意

- 时间列是月：`OS_Months`、`PFS_Months`；事件列是 `OS_Event`、`PFS_Event`。
- 不要把“响应分类”和“生存预测”混成一个指标。
- Cox 的 C-index 和分类的 AUROC 不是一回事。

### 交付

- `notebooks/w03_survival.ipynb`
- `results/survival_metrics.csv`
- 一张 KM 图 + 一张 C-index 对比表

---

## 第 4 周（20 小时）：PyTorch 基础 + MLP 基线

### 学习目标

- 理解 tensor、autograd、`nn.Module`、`Dataset`/`DataLoader`、训练循环、早停。
- 能训练一个表格 MLP，并与第 2 周的 sklearn 基线比较。

### 任务

- [ ] PyTorch 官方 60 分钟教程：tensor、autograd、`nn.Module`。
- [ ] 手写训练循环：forward、loss、backward、optimizer.step、zero_grad。
- [ ] 用 `Dataset`/`DataLoader` 包装 Chowell 数据。
- [ ] 训练 MLP（例如 2 层 hidden + dropout），做二分类 Response。
- [ ] 用验证集早停；测试集只评估一次。
- [ ] 记录训练曲线（loss/epoch）。
- [ ] 与第 2 周最好的基线对比，写入 `results/baseline_metrics.csv`（新增一行 `MLP`）。

### 交付

- `notebooks/w04_mlp.ipynb`
- 训练曲线图
- 一行 MLP 的测试集 AUROC + 置信区间
- 周会 5 页

### 第 4 周周末检查点（通过才进第 5 周）

能不看笔记回答：

1. `[Key, Value]` 里的 Key 和 Value 分别怎么变成向量？
2. 为什么论文的 transformer 不加位置编码？
3. `[TASK]` 和 `[MASK]` 各自在预训练/微调中做什么？
4. 你的 MLP 和 logistic 基线，谁更好？为什么？
5. 从干净环境重跑一遍，能复现你的数字吗？

---

## 每周固定动作

- 周一：写本周 1 个可验收目标（一个数字/一张图）。
- 周五：更新 `results/`，重启并运行全部 notebook。
- 周六：3 页周会 + commit + push。
- 每周至少记录一次“本周失败/卡点”，写进周会第 3 页。

## 不要做的事

- 不要先花两个月系统学完 Python 再碰数据。
- 不要同时学 R 的 torch 和 Python 的 PyTorch。
- 不要碰医院数据，直到第 8–10 周拿到数据字典并确认合规。
- 不要在测试集上反复调参。
- 不要追求 SOTA；这个阶段的目标是“可复现、能解释”。
