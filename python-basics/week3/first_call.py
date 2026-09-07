import os
import requests

# API_KEY = os.environ.get("DEEPSEEK_API_KEY")
API_KEY = "sk-3afac6102f8c4a9a92261776a6696b37"

if not API_KEY:
    print("❌ 错误：未找到 DEEPSEEK_API_KEY 环境变量")
    print("请先设置环境变量：set DEEPSEEK_API_KEY=your_key_here")
    exit(1)

URL = "https://api.deepseek.com/chat/completions"

resp = requests.post(
    URL,
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个严谨的金融分析助手，回答简洁专业。"},
            {"role": "user", "content": "用三句话解释什么是 RAG"},
        ],
        "stream": False,
    },
    timeout=60,
)

print("HTTP 状态码：", resp.status_code)

# ✅ 先检查状态码
if resp.status_code != 200:
    print("❌ API 调用失败")
    error_data = resp.json()
    print("错误信息：", error_data)
    # 打印完整响应以便调试
    print("完整响应：", resp.text)
    exit(1)

# 只有状态码为 200 时才解析正常响应
data = resp.json()
answer = data["choices"][0]["message"]["content"]
print("模型回答：", answer)
print("token 用量：", data["usage"])

"""
HTTP 状态码： 200
模型回答： RAG（检索增强生成）是一种将外部知识检索与大语言模型生成相结合的技术。  
它先根据用户问题从知识库中检索相关文档片段，再将这些片段作为上下文输入模型生成答案。  
这种方法能减少幻觉、提升回答准确性，并支持基于私有或实时数据的问答。
token 用量： {'prompt_tokens': 23, 'completion_tokens': 63, 'total_tokens': 86, 'prompt_tokens_details': {'cached_tokens': 0}, 'prompt_cache_hit_tokens': 0, 'prompt_cache_miss_tokens': 23}
"""


"""
(.venv) PS D:\ai-bootcamp> curl.exe -X POST https://api.deepseek.com/chat/completions `
>>   -H "Authorization: Bearer sk-3afac6102f8c4a9a92261776a6696b37" `
>>   -d '{\"model\":\"deepseek-chat\",\"messages\":[{\"role\":\"user\",\"content\":\"测试\"}],\"stream\":false}'
{"id":"c99ad6ce-9bdf-43a9-8191-e82db368a3c9","object":"chat.completion","created":1788760922,"model":"deepseek-v4-flash","choices":[{"index":0,"message":{"role":"assistant","content":"你好！很高兴见到你！😊\n\n我已经准备好了，随时可以帮你解答问题、提供建议或者进行各种对话。不管你有什么需要，尽管说：\n\n- 想聊点什么呢？\n- 需要帮忙解决什么问题吗？\n- 或者只是想找个人说说话？\n\n我都在这里等着你！✨\n\n有什么我可以帮你的吗？"},"logprobs":null,"finish_reason":"stop"}],"usage":{"prompt_tokens":5,"completion_tokens":70,"total_tokens":75,"prompt_tokens_details":{"cached_tokens":0},"prompt_cache_hit_tokens":0,"prompt_cache_miss_tokens":5},"system_fingerprint":"a26a7955944dc5c60445bff77fac9c8e"}
"""