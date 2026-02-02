import json
import allure
from api_autotest.clients.api_client import ApiResponse


def attach_request(method: str, url: str, headers: dict = None, body: any = None):
    """附加请求信息到 Allure 报告"""
    content = f"Method: {method}\nURL: {url}\n"
    if headers:
        # 脱敏：隐藏 token
        safe_headers = {k: ("***" if "authorization" in k.lower() else v) for k, v in headers.items()}
        content += f"Headers: {json.dumps(safe_headers, indent=2, ensure_ascii=False)}\n"
    if body:
        content += f"Body: {json.dumps(body, indent=2, ensure_ascii=False)}\n"
    allure.attach(content, name="Request", attachment_type=allure.attachment_type.TEXT)


def attach_response(resp: ApiResponse):
    """附加响应信息到 Allure 报告"""
    content = f"Status Code: {resp.status_code}\n"
    if resp.json:
        content += f"Response JSON:\n{json.dumps(resp.json, indent=2, ensure_ascii=False)}\n"
    else:
        content += f"Response Text: {resp.text[:500]}\n"  # 截断防止太长
    allure.attach(content, name="Response", attachment_type=allure.attachment_type.TEXT)