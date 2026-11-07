# Git 日常操作

> Git 只管理代码、notebook、结果表和文档；`data/raw/` 和 `data/processed/` 里的数据不提交。

## 每天开始（可选）

如果配置了 GitHub 远程仓库，先同步：

```powershell
cd "D:\TJH课题工作内容\clinicaltransformer\studyplan"
git pull
```

只有一台电脑、没有远程仓库时，可跳过。

## 每天结束

```powershell
cd "D:\TJH课题工作内容\clinicaltransformer\studyplan"
git status
git add .
git commit -m "week 1: Chowell EDA"
git push
```

说明：

- `git status`：先看改了哪些文件，确认没有数据文件/患者信息。
- `git add .`：把改动加入暂存区；`.gitignore` 会自动排除数据、`.Rhistory`、`__pycache__` 等。
- `git commit -m "..."`：在本地保存一个版本。
- `git push`：上传到 GitHub；没有远程仓库时会报错，可先不运行。

## 查看历史

```powershell
git log --oneline
git show <commit-id>
```

## 恢复旧版本

恢复某个文件到旧版本：

```powershell
git restore --source=<commit-id> path/to/file
```

把旧版本 notebook 导出成新文件：

```powershell
git show <commit-id>:notebooks/week01/week1_eda.ipynb > w01_old.ipynb
```

## 数据不在 Git 里

- Chowell 原始数据在 `data/raw/`，被 `.gitignore` 排除。
- 换电脑后重新下载：

```powershell
conda activate ctlearn
$env:HF_ENDPOINT = "https://hf-mirror.com"
python src/load_chowell.py
```

- 导师给的直肠癌数据只放医院批准的位置，永远不要提交到 Git。

## 提交信息建议

```text
week 0: environment + data
week 1: Chowell EDA
week 2: logistic baseline
week 3: survival analysis
week 4: PyTorch MLP
```
