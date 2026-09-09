"""embed_demo.py：文本 → 向量"""
import os
import requests

# API_KEY = os.environ["SILICONFLOW_API_KEY"]
API_KEY = "sk-wectwyauqkgjgzbzqhyrhapcwmwartboitmhwnwtrydpqhov"
URL = "https://api.siliconflow.cn/v1/embeddings"
MODEL = "BAAI/bge-m3"          # 免费中文向量模型

def embed(texts):
    """texts 是字符串列表，返回向量列表"""
    resp = requests.post(
        URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": MODEL, "input": texts, "encoding_format": "float"},
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()["data"]
    # 返回顺序和输入顺序一致，按 index 排序取 embedding
    return [d["embedding"] for d in sorted(data, key=lambda x: x["index"])]

# 语义相近的 3 组句子
sentences = [
    "苹果很好吃",
    "香蕉很甜我喜欢",
    "汽车价格不便宜",
]
vecs = embed(sentences)
print("每个向量维度：", len(vecs[0]))     # bge-m3 是 1024 维

def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return dot / (na * nb)

print("句1 vs 句2（水果类）:", round(cosine_similarity(vecs[0], vecs[1]), 4))
print("句1 vs 句3（跨类）  :", round(cosine_similarity(vecs[0], vecs[2]), 4))

"""
每个向量维度： 1024
句1 vs 句2（水果类）: 0.7149
句1 vs 句3（跨类）  : 0.4208
"""