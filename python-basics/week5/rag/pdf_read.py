"""pdf_read.py：读 PDF 并打印前几段文本"""
from pathlib import Path
from pypdf import PdfReader

pdf_path = Path("corpus/sample.pdf")   # 换成你的文件名
reader = PdfReader(str(pdf_path))
print(f"共 {len(reader.pages)} 页")

full_text = []
for i, page in enumerate(reader.pages):
    text = page.extract_text() or ""   # 某些扫描版 PDF 提取为空
    full_text.append(text)

text = "\n".join(full_text)
print("总字符数：", len(text))
print("======== 前 500 字预览 ========")
print(text[:500])