"""resume_parser.py：从简历文本提取结构化信息"""
import json
import os
import requests

API_KEY = os.environ["DEEPSEEK_API_KEY"]

resume_text = """
张三，男，1995 年 6 月生，本科毕业于上海大学计算机专业。
5 年 Python 后端开发经验，精通 FastAPI、Docker、MySQL。
曾就职于某券商，负责行情数据接口开发，有金融系统经验。
熟悉 RAG 与 LangChain，最近在做大模型应用。
"""

resp = requests.post(
    "https://api.deepseek.com/chat/completions",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content":
             "你是信息抽取引擎。从用户给的简历中提取信息，只输出 JSON，不要任何解释。"},
            {"role": "user", "content": resume_text},
        ],
        "response_format": {"type": "json_object"},   # ★ 开启 JSON mode
        "temperature": 0,      # 稳定输出，抽取得分毫不差
        "stream": False,
    },
    timeout=60,
)

raw = resp.json()["choices"][0]["message"]["content"]
print("模型原始输出：", raw)

# 关键一步：json.loads 必须能成功
data = json.loads(raw)     # 失败会抛 JSONDecodeError，企业应用必须保证这行不出错
print("\n解析后的字段：")
print("姓名：", data.get("name"))
print("技能：", data.get("skills"))