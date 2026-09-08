"""tests/test_smoke.py：上线前冒烟测试（本地跑）"""
import requests

BASE = "http://127.0.0.1:8000"

def test_health():
    r = requests.get(f"{BASE}/docs")
    assert r.status_code == 200

def test_chat_flow():
    r = requests.post(f"{BASE}/chat", json={"message": "你好"})
    assert r.status_code == 200
    data = r.json()
    assert "reply" in data and "session_id" in data
    sid = data["session_id"]
    # 记忆测试
    r2 = requests.post(f"{BASE}/chat",
                       json={"message": "我叫丹尼尔", "session_id": sid})
    r3 = requests.post(f"{BASE}/chat",
                       json={"message": "我叫什么", "session_id": sid})
    assert "丹尼尔" in r3.json()["reply"]
    print("冒烟测试全部通过 ✓")

if __name__ == "__main__":
    test_health()
    test_chat_flow()