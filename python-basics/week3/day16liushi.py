"""chat.py：多轮对话 + 流式输出（完整版）"""
import json
import os
import requests

API_KEY = os.environ["DEEPSEEK_API_KEY"]
URL = "https://api.deepseek.com/chat/completions"

messages = [
    {"role": "system", "content": "你是 Daniel 的 AI 学习助手，回答简洁专业，用中文。"}
]

def chat_once(user_input):
    """发送一轮请求，流式打印，返回完整回答"""
    messages.append({"role": "user", "content": user_input})

    resp = requests.post(
        URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": "deepseek-chat", "messages": messages, "stream": True},
        stream=True,
        timeout=120,
    )
    if resp.status_code != 200:
        print(f"请求失败：{resp.status_code} {resp.text}")
        messages.pop()          # 失败就把刚加的 user 撤掉，避免脏历史
        return None

    print("AI> ", end="", flush=True)
    full_reply = ""
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
        except (json.JSONDecodeError, KeyError, IndexError):
            continue
        piece = delta.get("content", "")
        if piece:
            full_reply += piece
            print(piece, end="", flush=True)
    print()

    if full_reply:
        messages.append({"role": "assistant", "content": full_reply})
    return full_reply

print("AI 助手已就绪（流式版）· 输入 exit 退出 · 输入 /clear 清空历史")
while True:
    user_input = input("\n你> ").strip()
    if user_input in ("exit", "quit"):
        break
    if user_input == "/clear":
        messages.clear()
        messages.append({"role": "system",
                         "content": "你是 Daniel 的 AI 学习助手，回答简洁专业，用中文。"})
        print("历史已清空")
        continue
    if user_input:
        chat_once(user_input)

"""
AI 助手已就绪（流式版）· 输入 exit 退出 · 输入 /clear 清空历史

你> 用一句话介绍什么是生成式 AI
AI> 生成式 AI 是一种能学习数据规律，并据此自主生成新内容（如文本、图像、音频等）的人工智能技术。

你> exit
"""