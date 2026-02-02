from api_autotest.clients.api_client import ApiClient


class AuthService:
    def __init__(self, client: ApiClient):
        self.client = client

    def login(self, username: str, password: str) -> str:
        resp = self.client.post("/login", json={"username": username, "password": password})
        assert resp.status_code == 200, f"login failed: {resp.status_code} {resp.text}"
        token = resp.json["access_token"]
        return token