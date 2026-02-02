from api_autotest.clients.api_client import ApiClient


class ItemService:
    def __init__(self, client: ApiClient):
        self.client = client

    def create_item(self, name: str, price: float, desc: str | None = None):
        return self.client.post("/items", json={"name": name, "price": price, "desc": desc})

    def get_item(self, item_id: int):
        return self.client.get(f"/items/{item_id}")

    def update_item(self, item_id: int, **fields):
        return self.client.patch(f"/items/{item_id}", json=fields)

    def delete_item(self, item_id: int):
        return self.client.delete(f"/items/{item_id}")