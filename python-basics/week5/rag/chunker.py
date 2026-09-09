"""chunker.py：把长文本切成带重叠的小块"""
import re

def split_by_paragraphs(text: str) -> list[str]:
    """先把文本按空行/换行切成段落，过滤太短的碎片"""
    # 把连续空白（含换行）规整成段落分隔
    blocks = re.split(r"\n\s*\n", text)
    paras = [b.strip() for b in blocks if len(b.strip()) > 20]
    return paras

def merge_paragraphs(paras: list[str], max_chars: int = 500,
                     overlap_chars: int = 50) -> list[str]:
    """把段落合并成 ≤max_chars 的块，块与块之间保留 overlap 重叠。

    设计说明：
    - 以段落为最小单元：同一段不拆开（保住完整语义）
    - 段落太长（超 max_chars）才按字符硬切
    - 相邻块尾部 50 字与下一块头部重复 → 观点跨块时不丢上下文
    """
    chunks = []
    current = ""
    for p in paras:
        if len(p) > max_chars:
            # 超长段落：先结算当前块，再单独硬切
            if current:
                chunks.append(current)
                current = ""
            for i in range(0, len(p), max_chars - overlap_chars):
                chunks.append(p[i:i + max_chars])
            continue
        if len(current) + len(p) + 1 > max_chars:
            # 当前块满了：把尾部 overlap_chars 字保留到下一块开头
            tail = current[-overlap_chars:] if current else ""
            chunks.append(current)
            current = tail + " " + p
        else:
            current = (current + " " + p).strip()
    if current:
        chunks.append(current)
    return chunks

def chunk_document(text: str) -> list[dict]:
    """完整分块：返回 [{chunk_text, chunk_index}] 列表"""
    paras = split_by_paragraphs(text)
    raw_chunks = merge_paragraphs(paras)
    return [{"chunk_text": c, "chunk_index": i} for i, c in enumerate(raw_chunks)]

# ===== 自测 =====
if __name__ == "__main__":
    from pathlib import Path
    from pypdf import PdfReader
    reader = PdfReader("corpus/sample.pdf")
    text = "\n".join((p.extract_text() or "") for p in reader.pages)
    chunks = chunk_document(text)
    print(f"共分出 {len(chunks)} 块")
    for c in chunks[:5]:
        print(f"\n--- 块 {c['chunk_index']}（前 50 字）---")
        print(c["chunk_text"][:50].replace("\n", " "))