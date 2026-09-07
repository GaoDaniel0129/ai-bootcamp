"""llm.py：所有 API 调用都在这里（主循环逻辑不碰 requests）"""
import json
import os
import requests

API_KEY = os.environ["DEEPSEEK_API_KEY"]
URL = "https://api.deepseek.com/chat/completions"

def chat(messages, with_tools=True):
    """一次请求，流式返回生成器；自动处理工具调用循环。"""
    payload = {"model": "deepseek-chat", "messages": messages,
               "stream": True, "temperature": 0}
    if with_tools:
        payload["tools"] = __import__("tools").TOOLS   # 避免循环 import 的取巧法
        # 更规范：from tools import TOOLS 放函数内部
    resp = requests.post(URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json=payload, stream=True, timeout=120)
    return resp

def parse_stream(resp):
    """把流式响应解析成 (完整文本, 工具调用列表)"""
    full_text = ""
    tool_calls = {}
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
            chunk = json.loads(payload)
            delta = chunk["choices"][0]["delta"]
        except (json.JSONDecodeError, KeyError, IndexError):
            continue
        if delta.get("content"):
            piece = delta["content"]
            full_text += piece
            print(piece, end="", flush=True)
        # 工具调用是分段到达的，按 index 累加拼装
        if delta.get("tool_calls"):
            for tc in delta["tool_calls"]:
                idx = tc["index"]
                tool_calls.setdefault(idx, {"id": "", "name": "", "args": ""})
                tool_calls[idx]["id"] += tc.get("id", "")
                tool_calls[idx]["name"] += tc.get("function", {}).get("name", "")
                tool_calls[idx]["args"] += tc.get("function", {}).get("arguments", "")
    print()
    return full_text, list(tool_calls.values())