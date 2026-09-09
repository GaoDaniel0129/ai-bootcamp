"""chroma_demo.py：Chroma 增查入门"""
import chromadb
import os

# 使用HF镜像站
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# 持久化客户端：数据存到 ./chroma_data 目录（重启不丢）
client = chromadb.PersistentClient(path="./chroma_data")

# 创建/获取集合（相当于"表"）
col = client.get_or_create_collection(name="reports")

# 添加：向量 + 文档原文 + id + 元数据
col.add(
    ids=["doc1", "doc2"],
    documents=["2025 年公司净利润同比增长 15%",
               "公司新发布 AI 产品，预计带来收入增长"],
    metadatas=[{"year": 2025}, {"year": 2025}],
    # embeddings 不传的话，Chroma 会用内置默认模型（英文为主）
    # 中文场景：用你 Day 29 的 BGE 向量，下一节接入
)

# 查询：语义找最像的
results = col.query(query_texts=["公司赚了多少钱"], n_results=2)
for doc, dist in zip(results["documents"][0], results["distances"][0]):
    print(f"距离 {dist:.3f} → {doc}")

"""
距离 0.216 → 公司新发布 AI 产品，预计带来收入增长
距离 0.504 → 2025 年公司净利润同比增长 15%
"""