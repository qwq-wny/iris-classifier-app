# 鸢尾花分类器（Iris Classifier App）


这是一个为大学课程做的小型机器学习项目。
应用根据 4 个测量值（花萼长度、花萼宽度、花瓣长度、花瓣宽度）
来预测鸢尾花的品种：山鸢尾（setosa）、变色鸢尾（versicolor）
或维吉尼亚鸢尾（virginica）。

项目完整展示了课程要求的整个工作流程：

- 训练好的机器学习模型（scikit-learn），
- 应用的自动化测试（pytest），
- Docker 容器化，
- 使用 GitHub Actions 的 CI/CD，
- 使用 DVC 进行数据版本管理，
- 使用 MLflow 记录机器学习实验。

## 应用的运行原理

1. 用户打开网页，输入 4 个数字。
2. 数字被送入一个逻辑回归模型。
3. 模型返回一个花的品种名称。

## 项目结构

```
app/                  Flask 网页应用
ml/                   训练代码、配置文件和 MLOps 文档
data/                 csv 数据文件（用 DVC 管理，不放进 git）
models/               保存好的模型（model.pkl）
tests/                pytest 测试
.github/workflows/    CI 和 CD 流水线
Dockerfile            构建应用镜像的说明文件
```

## 如何在自己的电脑上运行

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows 系统
pip install -r requirements.txt -r requirements-dev.txt
python -m ml.train --version improved
python -m app.main
```

然后在浏览器打开 http://127.0.0.1:5000

## 如何运行测试

```bash
pytest -v
```

## 如何用 Docker 运行

```bash
docker build -t iris-classifier-app .
docker run -p 5000:5000 iris-classifier-app
```

## 数据是如何做版本管理的（DVC）

csv 数据文件放在 `data/` 文件夹里，但它们**不**保存在 git 中。
git 只保存一个很小的指针文件 `data.dvc`。
真正的数据文件保存在 Azure Storage 的存储容器中。

下载数据的方法：

```bash
pip install -r requirements-dev.txt
dvc pull
```

更多说明：[ml/README_data.md](ml/README_data.md)

## 实验是如何记录的（MLflow）

每一次训练都会记录到 MLflow（保存在 `mlruns/` 文件夹）。
用一个简单的界面查看所有实验：

```bash
mlflow ui
```

然后打开 http://127.0.0.1:5000

更多说明：[ml/README_experiments.md](ml/README_experiments.md)

## 代码是如何从提交走向生产的

1. 新的开发工作在 `feature/...` 分支上进行。
2. 通过 Pull Request 把 feature 分支合并进 `dev`。
   此时会运行 CI：测试 + 代码检查 + Docker 构建。
   只有 CI 全部通过（绿色），Pull Request 才能合并。
3. 通过 Pull Request 把 `dev` 合并进 `staging`。
   staging 流水线会用 GitHub Secrets 生成 staging 环境的 `.env` 文件，
   并构建 staging 镜像。
4. 通过 Pull Request 把 `staging` 合并进 `main`。
   生产流水线会生成生产环境的 `.env` 文件，并构建生产镜像。

| 分支 | 用途 | 会运行的流水线 |
|---|---|---|
| feature/... | 开发新功能 | CI（打开 PR 时运行） |
| dev | 合并各功能、运行测试 | 每次推送和 PR 都运行 CI |
| staging | 像生产环境一样测试应用 | PR 时运行 CI + 合并时构建 staging 镜像 |
| main | 最终正式版本 | PR 时运行 CI + 合并时构建生产镜像 |

更多说明：[DEPLOYMENT.md](DEPLOYMENT.md)
