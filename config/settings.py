import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "http://127.0.0.1:8000")
    username: str = os.getenv("TEST_USERNAME", "testuser")  # 改这里
    password: str = os.getenv("TEST_PASSWORD", "testpass")  # 改这里
    timeout: float = float(os.getenv("TIMEOUT", "10"))

settings = Settings()