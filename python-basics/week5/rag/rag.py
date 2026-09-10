"""rag.py：手写 RAG 全链路（无框架版）
用法：python rag.py "你的问题"
"""
import os
import sys
import requests
import chromadb
import embed_utils as emb

# ---- 配置 ----
# DEEPSEEK_KEY = os.environ["DEEPSEEK_API_KEY"]
DEEPSEEK_KEY = "sk-3afac6102f8c4a9a92261776a6696b37"
LLM_URL = "https://api.deepseek.com/chat/completions"
COLLECTION = "reports"
TOP_K = 5

client = chromadb.PersistentClient(path="./chroma_data")
col = client.get_or_create_collection(name=COLLECTION)

def retrieve(question: str, k: int = TOP_K):
    """检索：问题 → 向量 → top-k 文本 + 距离"""
    q_vec = emb.embed_texts([question])
    res = col.query(query_embeddings=q_vec, n_results=k)
    docs = res["documents"][0]
    metas = res["metadatas"][0]
    dists = res["distances"][0]
    return list(zip(docs, metas, dists))

def build_prompt(question: str, hits) -> str:
    """拼 prompt：检索片段用编号列出来，要求模型只依据片段回答并标注引用"""
    context = "\n\n".join(
        f"[片段{i+1}] {doc}" for i, (doc, _, _) in enumerate(hits))
    return f"""请根据下面提供的【参考资料】回答问题。

【参考资料】
{context}

【问题】{question}

要求：
1. 只依据参考资料回答，资料里没有的信息就说"资料中未提及"；
2. 回答末尾用 [片段x] 标注依据了哪个片段。
"""

def generate(prompt: str) -> str:
    resp = requests.post(
        LLM_URL,
        headers={"Authorization": f"Bearer {DEEPSEEK_KEY}"},
        json={"model": "deepseek-chat",
              "messages": [{"role": "system", "content":
                            "你是严谨的金融问答助手，只依据资料作答。"},
                           {"role": "user", "content": prompt}],
              "temperature": 0.2, "stream": False},
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def rag(question: str):
    hits = retrieve(question)
    prompt = build_prompt(question, hits)
    answer = generate(prompt)

    print("问题：", question)
    print("\n【回答】\n", answer)
    print("\n【引用的原文片段】")
    for i, (doc, meta, dist) in enumerate(hits[:3], 1):
        print(f"\n[片段{i}] 距离{dist:.3f} 来源:{meta['source']}")
        print(" ", doc[:100].replace("\n", " "))

if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "2024 年证券行业营收增速是多少"
    rag(q)

"""
问题： 2024 年证券行业营收增速是多少

【回答】
 资料中未提及。[片段1][片段2][片段3]

【引用的原文片段】

[片段1] 距离1.008 来源:sample.pdf
  券 15 839316 长城网科 金元证券 2 831464 ST 创高智 国融证券 16 839332 ST 和海益 太平洋证券 3 831614 合富新材 光大证券 17839503 嘉能未来 

[片段2] 距离1.053 来源:sample.pdf
  4 广尔数码 开源证券 26 874052 优优汇联 太平洋证券 13 838723 ST 银联信 国联民生承 销保荐 27 874088 诺丽科技 开源证券 14 839143 ST 居易 湘财证券

[片段3] 距离1.165 来源:sample.pdf
  - 1 - 全 国 股 转 公 司 文 件 股转公告〔2026〕289 号 关于对未按规定披露 2026 年半年度报告 挂牌公司股票实施停牌的公告 截至 2026 年 8 月 31 日，除已提交主动终
"""