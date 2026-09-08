"""llm.py：LLM 调用（从 W3 bot 改造而来）"""
import os
import requests

API_KEY = os.environ["DEEPSEEK_API_KEY"]
URL = "https://api.deepseek.com/chat/completions"

def ask_llm(messages):
    """非流式调用，返回回答文本"""
    resp = requests.post(
        URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": "deepseek-chat", "messages": messages,
              "stream": False, "temperature": 0.7},
        timeout=120,
    )
    resp.raise_for_status()       # 非 2xx 直接抛异常
    return resp.json()["choices"][0]["message"]["content"]