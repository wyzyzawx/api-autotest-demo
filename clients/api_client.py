from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

import allure
import requests

from api_autotest.config.settings import settings


@dataclass
class ApiResponse:
    status_code: int
    json: Any
    text: str
    headers: Dict[str, str]
    request_method: str = ""
    request_url: str = ""
    request_body: Any = None


class ApiClient:
    def __init__(self, base_url: str | None = None, timeout: float | None = None):
        self.base_url = (base_url or settings.base_url).rstrip("/")
        self.timeout = timeout or settings.timeout
        self.session = requests.Session()
        self._token: Optional[str] = None

    def set_token(self, token: str | None):
        self._token = token

    def _make_headers(self, headers: Optional[dict] = None) -> dict:
        h = {"Accept": "application/json", "Content-Type": "application/json"}
        if self._token:
            h["Authorization"] = f"Bearer {self._token}"
        if headers:
            h.update(headers)
        return h

    def request(self, method: str, path: str, **kwargs) -> ApiResponse:
        url = f"{self.base_url}{path}"
        headers = self._make_headers(kwargs.pop("headers", None))
        body = kwargs.get("json")

        # 记录请求到 Allure
        self._attach_request(method, url, headers, body)

        resp = self.session.request(method, url, headers=headers, timeout=self.timeout, **kwargs)

        try:
            body_json = resp.json()
        except Exception:
            body_json = None

        api_resp = ApiResponse(
            status_code=resp.status_code,
            json=body_json,
            text=resp.text,
            headers=dict(resp.headers),
            request_method=method,
            request_url=url,
            request_body=body,
        )

        # 记录响应到 Allure
        self._attach_response(api_resp)

        return api_resp

    def _attach_request(self, method: str, url: str, headers: dict, body: any):
        """附加请求到 Allure（脱敏处理）"""
        safe_headers = {k: ("***" if "authorization" in k.lower() else v) for k, v in headers.items()}
        content = f"🔹 {method} {url}\n"
        content += f"Headers: {json.dumps(safe_headers, indent=2, ensure_ascii=False)}\n"
        if body:
            content += f"Body: {json.dumps(body, indent=2, ensure_ascii=False)}"
        allure.attach(content, name="📤 Request", attachment_type=allure.attachment_type.TEXT)

    def _attach_response(self, resp: ApiResponse):
        """附加响应到 Allure"""
        content = f"Status: {resp.status_code}\n"
        if resp.json:
            content += f"Body:\n{json.dumps(resp.json, indent=2, ensure_ascii=False)}"
        else:
            content += f"Text: {resp.text[:1000]}"
        allure.attach(content, name="📥 Response", attachment_type=allure.attachment_type.TEXT)

    def get(self, path: str, **kwargs) -> ApiResponse:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> ApiResponse:
        return self.request("POST", path, **kwargs)

    def patch(self, path: str, **kwargs) -> ApiResponse:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs) -> ApiResponse:
        return self.request("DELETE", path, **kwargs)