"""auth.py：JWT 签发与校验"""
import os
import jwt
from datetime import datetime, timedelta, timezone

SECRET = os.environ.get("JWT_SECRET", "dev-secret-change-me")  # 生产必须从环境变量读！
ALGO = "HS256"

def create_token(user_id: int, username: str) -> str:
    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),  # 24 小时过期
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, SECRET, algorithm=ALGO)

def decode_token(token: str) -> dict:
    """解析 token，失败/过期抛 jwt.PyJWTError"""
    return jwt.decode(token, SECRET, algorithms=[ALGO])