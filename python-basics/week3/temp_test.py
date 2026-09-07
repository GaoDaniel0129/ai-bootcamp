import os
import requests

API_KEY = os.environ["DEEPSEEK_API_KEY"]

def ask(temperature):
    resp = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "deepseek-chat",
            "messages": [{"role": "user",
                          "content": "给一款新的AI学习App起3个名字，直接输出名字"}],
            "temperature": temperature,
            "stream": False,
        },
        timeout=60,
    )
    return resp.json()["choices"][0]["message"]["content"].strip()

print("=== temperature = 0（确定性）5 次 ===")
for i in range(5):
    print(f"第{i+1}次:", ask(0))

print("\n=== temperature = 1（随机性）5 次 ===")
for i in range(5):
    print(f"第{i+1}次:", ask(1))