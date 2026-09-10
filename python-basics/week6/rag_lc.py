"""rag_lc.py：LangChain 版 RAG（功能对齐 W5 rag.py）"""
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

embeddings = OpenAIEmbeddings(model="BAAI/bge-m3",
    api_key=os.environ["SILICONFLOW_API_KEY"],
    base_url="https://api.siliconflow.cn/v1")
vectorstore = Chroma(persist_directory="./chroma_lc",
    embedding_function=embeddings, collection_name="reports_lc")
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})   # Top-5

llm = ChatOpenAI(model="deepseek-chat",
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com/v1", temperature=0.2)

prompt = ChatPromptTemplate.from_messages([
    ("system", """你是严谨的金融问答助手。
请只依据下面的【资料】回答问题：
{context}
资料里没有的信息，回答"资料中未提及"。
回答末尾标注依据的片段来源，如 [source: 文件名]"""),
    ("human", "{question}"),
])

def format_docs(docs):
    """把检索结果拼成上下文（带来源标注）"""
    return "\n\n".join(
        f"[{d.metadata.get('source','?')}] {d.page_content}" for d in docs)

# LCEL 链：question 透传 + 检索(context) + 生成
chain = (
    {"context": retriever | format_docs,      # retriever 结果先格式化
     "question": RunnablePassthrough()}       # 原样透传
    | prompt
    | llm
    | StrOutputParser()
)

answer = chain.invoke("2024 年证券行业营收同比增速是多少？")
print(answer)