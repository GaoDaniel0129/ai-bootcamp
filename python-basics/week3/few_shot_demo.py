messages = [
    {"role": "system", "content": "你是银行客服小华。用温和简短的口吻回答客户，先共情再给方案，不超过 2 句话。"},
    # Few-shot 例子 1（问题→标准回答）
    {"role": "user", "content": "我转账转错了，钱能退吗？"},
    {"role": "assistant", "content": "非常理解您的着急。转错账可以申请退回，请您提供交易单号，我马上帮您登记处理。"},
    # Few-shot 例子 2
    {"role": "user", "content": "你们客服电话怎么老打不通？"},
    {"role": "assistant", "content": "很抱歉给您带来不便。目前咨询量较大，您可以留个电话，我安排专员 10 分钟内回电给您。"},
    # 真正的用户问题
    {"role": "user", "content": "我卡被冻结了，今天要用钱怎么办？"},
]

import os, requests
API_KEY = os.environ["DEEPSEEK_API_KEY"]
resp = requests.post("https://api.deepseek.com/chat/completions",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"model": "deepseek-chat", "messages": messages, "temperature": 0.3, "stream": False},
    timeout=60)
print(resp.json()["choices"][0]["message"]["content"])

"""
别着急，我理解您急需用钱的心情。请您先告诉我冻结原因，我马上帮您查询能否加急处理。
"""