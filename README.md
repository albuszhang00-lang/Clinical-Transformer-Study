# Clinical Transformer 学习项目（直肠癌方向）

> 目标：6 个月、每周 20 小时，从 R 背景转到 Python；先复现论文的表格 Clinical Transformer，再完成一个直肠癌预测模型。

## 1. 先记住三件事

1. **论文的 Clinical Transformer 不是文本模型。** 输入是 `[Key, Value]` 表格特征（TMB、NLR、白蛋白、MSI 等），做特征名 + 数值 embedding；预训练任务是 mask 特征名，微调用 `[TASK]` token 做生存/分类。
2. **论文做的是疗效/生存，不是 irAE。** irAE 不是第一阶段目标。
3. **先基线后模型。** logistic / Cox / XGBoost 必须先跑；transformer 不天然更好。

## 2. 20 周路线

| 阶段 | 周 | 内容 | 验收 |
|---|---|---|---|
| 0 环境 | 0 | 安装、GitHub、SSH 医院 GPU、下载 Chowell 数据 | `check_env.py` 全 OK，CSV 落地 |
| 1 基础 | 1–4 | Python → pandas → sklearn → 生存分析 → PyTorch MLP | 4 个 notebook + 基线指标表 |
| 2 复现 | 5–9 | 读论文/代码 → 实现 `[Key,Value]` Transformer → 分类/生存头 → 与基线对比 | 一个复现指标 + 消融表 |
| 3 直肠癌代理 | 10–14 | 公开直肠癌数据（GSE68204 / GSE119409 / GSE242786） | 数据字典 + 基线 vs CT |
| 4 自有数据/收尾 | 15–20 | 导师数据到位后替换；否则完成迁移方案 + 报告 | 10–15 页报告 + 仓库 |

**关键检查点：** 第 8–10 周向导师要一份数据字典/样本清单，确认数据类型、样本量、pCR/TRG 标签和可访问时间。数据在导师手里不等于你已经知道它长什么样。

## 3. 目录结构

```
clinical-transformer-learning/
├── README.md
├── environment.yml          # conda 环境
├── requirements.txt         # pip 备用
├── docs/
│   ├── week0-4_plan.md      # 前 5 周逐周任务
│   └── group_meeting_template.md
├── data/
│   ├── raw/                 # 原始数据（不提交到 git）
│   └── processed/           # 处理后的数据（不提交）
├── notebooks/               # 每周 notebook
├── results/                 # 指标表、图
└── src/
    ├── check_env.py         # 环境自检
    └── load_chowell.py      # 下载 Chowell 数据
```

## 4. 第 0 周安装（Windows）

### 4.1 装工具

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html)（Python 环境）
- [VS Code](https://code.visualstudio.com/)（编辑器）
- [Git](https://git-scm.com/)（版本控制）
- GitHub 账号（私有仓库即可）

### 4.2 创建环境

打开 **Anaconda PowerShell Prompt**，进入本项目目录：

```powershell
cd clinical-transformer-learning
conda env create -f environment.yml
conda activate ctlearn
python src/check_env.py
python src/load_chowell.py
```

如果 `conda` 命令找不到，先运行 `conda init powershell`，然后重开终端。
后续每次要继续任务就运行
  cd "D:\TJH课题工作内容\clinicaltransformer\studyplan"
  conda activate ctlearn
  python src/check_env.py
如果提示符是base而不是ctlearn
  conda activate ctlearn

### 4.3 国内下载 Hugging Face 数据

如果 `load_chowell.py` 下载很慢或超时，先设置镜像：

```powershell
$env:HF_ENDPOINT = "https://hf-mirror.com"
python src/load_chowell.py
```

### 4.4 安装 PyTorch（CPU 版，可选）

第 4 周才需要。Windows 笔记本建议先装 CPU 版，避免几个 GB 的 CUDA 依赖：

```powershell
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### 4.5 连医院 GPU

```powershell
ssh <用户名>@<医院服务器地址>
nvidia-smi
```

在 VS Code 里安装 **Remote - SSH** 扩展，连上服务器后把本项目同步过去，再在服务器上建同样的 conda 环境。训练放服务器，编辑和调试可以留在本地。

### 4.6 初始化 Git

```powershell
git init
git add .
git commit -m "week 0: project scaffold"
git branch -M main
git remote add origin <你的仓库地址>
git push -u origin main
```

## 5. 数据使用规则

- **Chowell 数据**：公开数据，可以下载；`data/raw/` 和 `data/processed/` 不提交到 git。
- **导师手里的直肠癌数据**：只在医院批准的内网/服务器上处理；个人电脑不存可识别信息；不把数据上传到任何公开网盘或第三方网站。
- 提交到 git 的只有代码、notebook、指标表和脱敏后的汇总结果。

## 6. 每周节奏

| 时间 | 动作 |
|---|---|
| 周一 | 写下本周 1 个可验收目标（一个数字/一张图） |
| 周二–周四 | 学习 + 写代码；卡住超过 2 小时就记录报错并求助 |
| 周五 | 更新 `results/` 指标表，重启并运行全部 notebook |
| 周六 | 准备周会 3 页，commit + push |
| 周日 | 休息 / 补进度 |

**周会规则：只展示能跑的东西和数字；不展示学习笔记；不贴没有数字的截图。**

## 7. 常见问题

| 问题 | 处理 |
|---|---|
| `conda` 不是内部或外部命令 | `conda init powershell`，重开终端 |
| Hugging Face 下载超时 | `$env:HF_ENDPOINT = "https://hf-mirror.com"` |
| `torch` 安装太大/太慢 | 用上面的 CPU wheel 命令 |
| VS Code 找不到 `ctlearn` 内核 | `python -m ipykernel install --user --name ctlearn` |
| 医院 GPU 暂时没开通 | 本地 CPU + Kaggle/Colab 免费 GPU，不要阻塞 |
| 报错看不懂 | 保存完整 traceback；先搜最后一行；再问 AI/导师 |

## 8. 下一步

1. 完成第 0 周验收。
2. 按 `docs/week0-4_plan.md` 执行第 1–4 周。
3. 第 4 周周末做一次自测；通过后再进入第 5 周的论文复现。
