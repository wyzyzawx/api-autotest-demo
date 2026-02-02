import os
import sys

# 确保项目根目录在 sys.path
PROJECT_ROOT = os.path.dirname(__file__)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
import allure

from clients.api_client import ApiClient
from config.settings import settings
from services.auth_service import AuthService
from services.item_service import ItemService


# ========== Allure 环境信息 ==========
def pytest_configure(config):
    """配置 Allure 环境信息"""
    allure_dir = config.getoption("--alluredir", default=None)
    if allure_dir:
        env_file = os.path.join(allure_dir, "environment.properties")
        os.makedirs(allure_dir, exist_ok=True)
        with open(env_file, "w") as f:
            f.write(f"Base.URL={settings.base_url}\n")
            f.write(f"Python.Version={sys.version}\n")
            f.write(f"Test.User={settings.username}\n")


# ========== Fixtures ==========
@pytest.fixture(scope="session")
def client() -> ApiClient:
    return ApiClient(base_url=settings.base_url, timeout=settings.timeout)


@pytest.fixture(scope="session")
def token(client: ApiClient) -> str:
    auth = AuthService(client)
    t = auth.login(settings.username, settings.password)
    return t


@pytest.fixture()
def authed_client(client: ApiClient, token: str) -> ApiClient:
    client.set_token(token)
    return client


@pytest.fixture()
def item_service(authed_client: ApiClient) -> ItemService:
    return ItemService(authed_client)


@pytest.fixture()
def created_item_id(item_service: ItemService):
    """创建一个 Item 用于测试，测试后自动清理"""
    from utils.data_factory import make_item

    data = make_item()

    with allure.step(f"[Setup] 创建测试 Item: {data.name}"):
        resp = item_service.create_item(data.name, data.price, data.desc)
        assert resp.status_code == 200, f"Setup failed: {resp.text}"
        item_id = resp.json["id"]
        allure.attach(str(item_id), name="Created Item ID", attachment_type=allure.attachment_type.TEXT)

    yield item_id

    # Teardown: 尝试删除（可能已被测试删除）
    with allure.step(f"[Teardown] 清理 Item {item_id}"):
        del_resp = item_service.delete_item(item_id)
        if del_resp.status_code == 200:
            allure.attach("Deleted successfully", name="Cleanup", attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach(f"Already deleted or not found: {del_resp.status_code}", name="Cleanup", attachment_type=allure.attachment_type.TEXT)