"""chain_demo.py：LCEL 一句话问答链"""
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. 模型（指向 DeepSeek——OpenAI 兼容，改 base_url）
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.environ["DEEPSEEK_API_KEY"],   # 前面补 import os
    base_url="https://api.deepseek.com/v1",
    temperature=0.3,
)

# 2. Prompt 模板（变量用 {name} 占位）
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是金融助手，用一句话回答。"),
    ("human", "{question}"),
])

# 3. 输出解析器（把模型返回的复杂对象变成纯字符串）
parser = StrOutputParser()

# 4. LCEL 管道：prompt → llm → parser 串起来，就是一个"链"
chain = prompt | llm | parser

# 5. 调用：只需传入模板变量
answer = chain.invoke({"question": "什么是 RAG？"})
print(answer)