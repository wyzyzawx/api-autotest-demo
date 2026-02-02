import pytest
import allure
from api_autotest.clients.api_client import ApiClient

pytestmark = [pytest.mark.regression]


@allure.epic("Auth API")
@allure.feature("Login Negative Cases")
class TestLoginNegative:
    """登录接口反例测试"""

    @pytest.fixture
    def client(self):
        return ApiClient()

    @allure.story("错误密码")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_password(self, client):
        """密码错误应返回 401"""
        with allure.step("使用错误密码登录"):
            r = client.post("/login", json={"username": "testuser", "password": "wrongpass"})

        with allure.step("验证返回 401"):
            assert r.status_code == 401

    @allure.story("错误用户名")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_username(self, client):
        """用户名错误应返回 401"""
        with allure.step("使用不存在的用户名登录"):
            r = client.post("/login", json={"username": "nouser", "password": "testpass"})

        with allure.step("验证返回 401"):
            assert r.status_code == 401

    @allure.story("参数缺失")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "payload, description",
        [
            ({"username": "testuser"}, "缺少 password"),
            ({"password": "testpass"}, "缺少 username"),
            ({}, "空 payload"),
            ({"username": "", "password": "testpass"}, "username 为空"),
            ({"username": "testuser", "password": ""}, "password 为空"),
        ],
    )
    def test_login_missing_fields(self, client, payload, description):
        """登录参数校验"""
        allure.dynamic.title(f"登录反例 - {description}")

        with allure.step(f"发送无效请求: {description}"):
            r = client.post("/login", json=payload)

        with allure.step("验证返回 422 或 401"):
            assert r.status_code in (401, 422)