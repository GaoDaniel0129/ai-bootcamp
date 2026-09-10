"""bm25_demo.py：关键词检索"""
import json
from pathlib import Path
from rank_bm25 import BM25Okapi

# 简单分词（中文：按字/词都行，这里用字符 bigram 近似 + 简单切词）
def tokenize(text):
    return list(text)          # 按单字切最简单；正式项目用 jieba

# 从 chroma 里把全部文档捞出来建 BM25 索引
import chromadb
client = chromadb.PersistentClient(path="./chroma_data")
col = client.get_or_create_collection(name="reports")
all_data = col.get(include=["documents"])
texts = all_data["documents"]
ids = all_data["ids"]
print(f"语料 {len(texts)} 块，建 BM25 索引...")

corpus_tokens = [tokenize(t) for t in texts]
bm25 = BM25Okapi(corpus_tokens)

def bm25_search(query, k=5):
    scores = bm25.get_scores(tokenize(query))
    top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
    return [(texts[i], scores[i]) for i in top_idx if scores[i] > 0]

for doc, score in bm25_search("证券行业营收同比增速", 3):
    print(f"BM25 {score:.1f} → {doc[:50].replace(chr(10),' ')}...")