import random
import string
from dataclasses import dataclass


def rand_str(prefix: str = "t", n: int = 8) -> str:
    s = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))
    return f"{prefix}_{s}"


@dataclass
class ItemData:
    name: str
    price: float
    desc: str


def make_item() -> ItemData:
    return ItemData(
        name=rand_str("item"),
        price=round(random.uniform(1, 999), 2),
        desc=rand_str("desc", 12),
    )