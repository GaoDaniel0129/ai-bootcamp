"""config.py：所有配置集中在这里，从环境变量读，绝不硬编码"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_FILE = DATA_DIR / "chat.db"
STATIC_DIR = Path(__file__).parent / "static"

DEEPSEEK_API_KEY = os.environ["DEEPSEEK_API_KEY"]       # 没有就报错，防漏配
JWT_SECRET = os.environ.get("JWT_SECRET", "dev-secret")
SYSTEM_PROMPT = "你是 Daniel 的 AI 助手，回答简洁专业，用中文。"
MODEL = "deepseek-chat"

def ensure_dirs():
    DATA_DIR.mkdir(exist_ok=True)