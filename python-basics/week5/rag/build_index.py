"""build_index.py：把 corpus 里所有 PDF 分块 → 向量化 → 入库"""
import chromadb
from pathlib import Path
from pypdf import PdfReader
import embed_utils as emb
from chunker import chunk_document

# ============ 修复：删除旧collection ============
client = chromadb.PersistentClient(path="./chroma_data")
try:
    client.delete_collection("reports")
    print("已删除旧的reports collection")
except Exception as e:
    print(f"删除collection时: {e}")

# 创建新collection，不指定embedding_function（因为手动传入向量）
col = client.create_collection(name="reports")
# ============ 修复结束 ============

def ingest_one_pdf(pdf_path: Path, batch_size: int = 16):
    """入库单份 PDF：分块 → 批量向量化 → add"""
    reader = PdfReader(str(pdf_path))
    text = "\n".join((p.extract_text() or "") for p in reader.pages)
    chunks = chunk_document(text)
    print(f"{pdf_path.name}: {len(chunks)} 块")

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        texts = [c["chunk_text"] for c in batch]
        vecs = emb.embed_texts(texts)  # 1024维向量
        
        # 现在手动传入向量，不会与collection的embedding冲突
        col.add(
            ids=[f"{pdf_path.stem}#{c['chunk_index']}" for c in batch],
            embeddings=vecs,  # 手动传入1024维向量
            documents=texts,
            metadatas=[{"source": pdf_path.name} for c in batch],
        )
    print(f"  ✓ 已入库 {len(chunks)} 块")

if __name__ == "__main__":
    corpus = Path("corpus")
    pdfs = list(corpus.glob("*.pdf"))
    print(f"发现 {len(pdfs)} 份 PDF")
    for p in pdfs:
        ingest_one_pdf(p)
    print(f"\n集合内总数: {col.count()}")