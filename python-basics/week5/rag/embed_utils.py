"""embed_utils.py：embedding 公共调用"""
import os
import requests

# API_KEY = os.environ["SILICONFLOW_API_KEY"]
API_KEY = "sk-wectwyauqkgjgzbzqhyrhapcwmwartboitmhwnwtrydpqhov"
URL = "https://api.siliconflow.cn/v1/embeddings"
MODEL = "BAAI/bge-m3"

def embed_texts(texts: list[str]) -> list[list[float]]:
    resp = requests.post(
        URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": MODEL, "input": texts, "encoding_format": "float"},
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()["data"]
    return [d["embedding"] for d in sorted(data, key=lambda x: x["index"])]

if __name__ == "__main__":
    v = embed_texts(["测试一下"])
    print("维度:", len(v[0]))