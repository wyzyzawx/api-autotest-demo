import pytest
import allure
from api_autotest.utils.data_factory import make_item

pytestmark = [pytest.mark.smoke]


@allure.epic("Items API")
@allure.feature("CRUD Operations")
@allure.story("Complete CRUD Flow")
@allure.severity(allure.severity_level.CRITICAL)
def test_items_crud_flow(item_service, created_item_id):
    """测试 Item 的完整 CRUD 流程"""

    with allure.step("1. 查询刚创建的 Item"):
        r_get = item_service.get_item(created_item_id)
        assert r_get.status_code == 200
        assert r_get.json["id"] == created_item_id

    with allure.step("2. 更新 Item 名称"):
        new_name = make_item().name
        r_upd = item_service.update_item(created_item_id, name=new_name)
        assert r_upd.status_code == 200
        assert r_upd.json["name"] == new_name

    with allure.step("3. 删除 Item"):
        r_del = item_service.delete_item(created_item_id)
        assert r_del.status_code == 200
        assert r_del.json["deleted"] is True

    with allure.step("4. 验证 Item 已被删除（应返回 404）"):
        r_get2 = item_service.get_item(created_item_id)
        assert r_get2.status_code == 404