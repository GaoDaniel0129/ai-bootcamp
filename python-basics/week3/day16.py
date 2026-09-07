"""chat.py：命令行多轮对话机器人"""
import os
import requests

# API_KEY = os.environ["DEEPSEEK_API_KEY"]
API_KEY = "sk-3afac6102f8c4a9a92261776a6696b37"
URL = "https://api.deepseek.com/chat/completions"

# 历史消息列表：第一项永远是 system（人设）
messages = [
    {"role": "system", "content": "你是 Daniel 的 AI 学习助手，回答简洁、专业、用中文。"}
]

print("AI 助手已就绪（输入 exit 退出）")
while True:
    user_input = input("\n你> ").strip()
    if user_input in ("exit", "quit"):
        print("再见！")
        break
    if not user_input:
        continue

    # 1. 把用户话加入历史
    messages.append({"role": "user", "content": user_input})

    # 2. 带着全部历史调 API
    resp = requests.post(
        URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": "deepseek-chat", "messages": messages, "stream": False},
        timeout=60,
    )
    data = resp.json()
    reply = data["choices"][0]["message"]["content"]

    # 3. 把模型回答也加入历史（关键！不加它模型就"失忆"）
    messages.append({"role": "assistant", "content": reply})

    print("AI>", reply)

"""
AI 助手已就绪（输入 exit 退出）

你> 你好，我叫丹尼尔
AI> 你好，丹尼尔！很高兴认识你。有什么我可以帮你的吗？

你> 我叫什么名字
AI> 你叫丹尼尔（Daniel），刚才你告诉我的。需要我帮你做点什么吗？

你> 我今年30 岁，在学AI
AI> 好的，丹尼尔。30岁学AI正当时——既有学习能力，又有实践经验。你目前是零基础入门，还是有一定基础？想从事哪个方向（比如机器学习、深度学习、AI应用开发等）？我可以帮你梳理学习路线或推荐资源。

你> 我几岁了
AI> 你今年30岁，丹尼尔。需要我帮你规划一些适合30岁起步的AI学习路径吗？

你> exit
再见！
"""