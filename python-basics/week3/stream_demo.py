import os
import requests

API_KEY = os.environ["DEEPSEEK_API_KEY"]
# API_KEY = "sk-3afac6102f8c4a9a92261776a6696b37"

resp = requests.post(
    "https://api.deepseek.com/chat/completions",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "从 1 数到 10，用逗号分隔"}],
        "stream": True,          # ★ 关键：开启流式
    },
    stream=True,                 # ★ requests 层也要开流，才能边收边读
    timeout=120,
)

# 逐行读取响应
for line in resp.iter_lines():
    if not line:
        continue                        # 跳过空行
    line = line.decode("utf-8")
    if not line.startswith("data:"):
        continue                        # 跳过非 data 行
    payload = line[5:].strip()          # 去掉 "data:" 前缀
    if payload == "[DONE]":
        break                           # 流结束标记
    import json
    chunk = json.loads(payload)         # 每块是一个 JSON
    delta = chunk["choices"][0]["delta"]
    content = delta.get("content", "")  # 用 .get 防报错（首块只有 role）
    print(content, end="", flush=True)  # flush=True 立即输出，不打折
print()

"""
1, 2, 3, 4, 5, 6, 7, 8, 9, 10
"""