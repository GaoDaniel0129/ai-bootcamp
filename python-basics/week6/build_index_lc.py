"""build_index_lc.py：LangChain 版入库（可对比 W5 build_index.py）"""
import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# Embedding 仍用 BGE（经硅基流动，OpenAI 兼容）
embeddings = OpenAIEmbeddings(
    model="BAAI/bge-m3",
    api_key=os.environ["SILICONFLOW_API_KEY"],
    base_url="https://api.siliconflow.cn/v1",
)

# 分块器：LangChain 版（recursive：优先按段落/句号切，比纯字符切聪明）
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,          # 和你 W5 的 max_chars 对齐
    chunk_overlap=50,        # 和你的 overlap 对齐
    separators=["\n\n", "\n", "。", "！", "？", " "],   # 中文句读优先
)

all_docs = []
for pdf in Path("corpus").glob("*.pdf"):
    loader = PyPDFLoader(str(pdf))
    pages = loader.load()                      # 每页一个 Document
    docs = splitter.split_documents(pages)     # 自动分块，带 metadata(source/page)
    for d in docs:
        d.metadata["source"] = pdf.name        # 记录来源文件名
    all_docs.extend(docs)
    print(f"{pdf.name}: {len(docs)} 块")

# 一键入库（内部自动向量化）
vectorstore = Chroma.from_documents(
    documents=all_docs,
    embedding=embeddings,
    persist_directory="./chroma_lc",           # 独立目录，与手写版并存
    collection_name="reports_lc",
)
print(f"共入库 {len(all_docs)} 块")