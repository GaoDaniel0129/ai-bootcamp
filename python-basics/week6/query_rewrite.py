"""query_rewrite.py：多轮问题改写"""
from langchain_openai import ChatOpenAI
import os

llm = ChatOpenAI(model="deepseek-chat",
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com/v1", temperature=0)

REWRITE_PROMPT = """你是检索助手。把用户最新问题改写成【可以独立检索】的完整问题。
规则：结合对话历史补全指代词（它/这个/那家），但不要添加历史里没有的信息。
只输出改写后的问题，不要解释。

【对话历史】
{history}

【最新问题】
{question}
"""

def rewrite(history: list[dict], question: str) -> str:
    hist_str = "\n".join(f"{m['role']}: {m['content']}" for m in history[-4:])
    resp = llm.invoke(REWRITE_PROMPT.format(history=hist_str, question=question))
    return resp.content.strip()

# 测试
history = [
    {"role": "user", "content": "茅台 2024 年毛利率是多少？"},
    {"role": "assistant", "content": "91.5%"},
]
q2 = "那五粮液呢？"
print("改写后：", rewrite(history, q2))
# 期望输出：五粮液 2024 年的毛利率是多少？