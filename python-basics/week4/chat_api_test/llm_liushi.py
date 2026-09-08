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


"""llm.py 追加：流式调用（生成器版）"""
def ask_llm_stream(messages):
    """yield 文本片段（不含 SSE 包装），由路由层负责包装"""
    resp = requests.post(
        URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": "deepseek-chat", "messages": messages,
              "stream": True, "temperature": 0.7},
        stream=True,
        timeout=120,
    )
    resp.raise_for_status()
    import json
    for line in resp.iter_lines():
        if not line:
            continue
        line = line.decode("utf-8")
        if not line.startswith("data:"):
            continue
        payload = line[5:].strip()
        if payload == "[DONE]":
            break
        try:
            delta = json.loads(payload)["choices"][0]["delta"]
        except Exception:
            continue
        piece = delta.get("content", "")
        if piece:
            yield piece