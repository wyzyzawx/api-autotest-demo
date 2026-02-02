# API 自动化测试项目

基于 **pytest + requests + Allure** 的接口自动化测试框架。

## 项目结构

```
api_autotest/
├── clients/          # 请求封装层
│   └── api_client.py
├── services/         # 业务封装层
│   ├── auth_service.py
│   └── item_service.py
├── config/           # 配置管理
│   └── settings.py
├── utils/            # 工具类
│   ├── data_factory.py
│   └── allure_helper.py
├── tests/            # 测试用例
│   ├── test_smoke_items.py
│   ├── test_negative_items.py
│   └── test_negative_login.py
├── conftest.py       # pytest fixtures
├── pytest.ini        # pytest 配置
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install pytest requests pydantic python-dotenv allure-pytest
```

### 2. 启动被测服务

```bash
cd demo-api
uvicorn main:app --reload --port 8000
```

### 3. 运行测试

```bash
# 运行 smoke 测试
pytest -m smoke --alluredir=allure-results

# 运行全部测试
pytest --alluredir=allure-results

# 查看报告
allure serve allure-results
```

## 用例分层

| 标签 | 说明 | 运行命令 |
|------|------|----------|
| smoke | 冒烟测试，核心流程 | `pytest -m smoke` |
| regression | 回归测试，含反例 | `pytest -m regression` |

## 环境配置

通过环境变量或 `.env` 文件配置：

```
BASE_URL=http://127.0.0.1:8000
TEST_USERNAME=testuser
TEST_PASSWORD=testpass
TIMEOUT=10
