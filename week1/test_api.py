import os
import requests

# 从环境变量获取API密钥
key = os.environ.get("DASHSCOPE_API_KEY")
if not key:
    print("错误：环境变量 DASHSCOPE_API_KEY 没设置")
    print("请在阿里云百炼控制台获取API Key：https://bailian.console.aliyun.com")
    exit(1)

# 通义百炼API端点
url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "qwen-plus",  # 可选: qwen-turbo, qwen-plus, qwen-max
    "messages": [
        {"role": "user", "content": "用一句话介绍你自己"}
    ],
    "temperature": 0.7
}

try:
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    
    # 打印调试信息
    print(f"状态码: {resp.status_code}")
    
    # 检查响应状态
    if resp.status_code == 200:
        data = resp.json()
        if "choices" in data and len(data["choices"]) > 0:
            print("\n回答:", data["choices"][0]["message"]["content"])
        else:
            print("响应格式异常:", data)
    else:
        # 打印错误详情
        print(f"请求失败，状态码: {resp.status_code}")
        print(f"错误信息: {resp.text}")
        
except requests.exceptions.Timeout:
    print("请求超时，请检查网络连接")
except requests.exceptions.RequestException as e:
    print(f"请求异常: {e}")