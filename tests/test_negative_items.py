import pytest
import allure
from api_autotest.clients.api_client import ApiClient
from api_autotest.services.item_service import ItemService
from api_autotest.config.settings import settings
from api_autotest.utils.data_factory import rand_str

pytestmark = [pytest.mark.regression]


@allure.epic("Items API")
@allure.feature("Negative Cases")
class TestCreateItemNegative:
    """创建 Item 的反例测试"""

    @allure.story("参数校验")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "payload, expected_status, description",
        [
            # 缺少必填字段
            ({"price": 12.3}, 422, "缺少 name 字段"),
            ({"name": "test"}, 422, "缺少 price 字段"),
            ({}, 422, "空 payload"),

            # name 字段校验
            ({"name": "", "price": 12.3}, 422, "name 为空字符串"),
            ({"name": "x" * 31, "price": 12.3}, 422, "name 超过最大长度"),

            # price 字段校验
            ({"name": "test", "price": 0}, 422, "price 为 0"),
            ({"name": "test", "price": -1}, 422, "price 为负数"),
            ({"name": "test", "price": 100000}, 422, "price 超过最大值"),
        ],
        ids=lambda x: x if isinstance(x, str) else None,
    )
    def test_create_item_invalid_payload(self, item_service, payload, expected_status, description):
        """测试创建 Item 时的参数校验"""
        allure.dynamic.title(f"创建 Item 反例 - {description}")

        with allure.step(f"发送无效请求: {description}"):
            r = item_service.client.post("/items", json=payload)

        with allure.step(f"验证返回状态码为 {expected_status}"):
            assert r.status_code == expected_status, f"Expected {expected_status}, got {r.status_code}"


@allure.epic("Items API")
@allure.feature("Authentication")
class TestAuthNegative:
    """鉴权反例测试"""

    @allure.story("未登录访问")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_item_without_token(self):
        """未登录时创建 Item 应返回 401"""
        client = ApiClient()  # 不设置 token

        with allure.step("不带 token 请求创建 Item"):
            r = client.post("/items", json={"name": "test", "price": 10.0})

        with allure.step("验证返回 401 Unauthorized"):
            assert r.status_code == 401

    @allure.story("无效 Token")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_item_with_invalid_token(self):
        """使用无效 token 应返回 401"""
        client = ApiClient()
        client.set_token("invalid-token-12345")

        with allure.step("使用无效 token 请求"):
            r = client.post("/items", json={"name": "test", "price": 10.0})

        with allure.step("验证返回 401"):
            assert r.status_code == 401


@allure.epic("Items API")
@allure.feature("Resource Not Found")
class TestNotFound:
    """资源不存在的测试"""

    @allure.story("查询不存在的 Item")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_nonexistent_item(self, item_service):
        """查询不存在的 Item 应返回 404"""
        with allure.step("查询一个不存在的 Item ID"):
            r = item_service.get_item(99999)

        with allure.step("验证返回 404"):
            assert r.status_code == 404

    @allure.story("删除不存在的 Item")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_nonexistent_item(self, item_service):
        """删除不存在的 Item 应返回 404"""
        with allure.step("删除一个不存在的 Item ID"):
            r = item_service.delete_item(99999)

        with allure.step("验证返回 404"):
            assert r.status_code == 404