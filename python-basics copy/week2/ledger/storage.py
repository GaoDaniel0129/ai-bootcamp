"""storage.py：负责把账目存到 JSON 文件、从文件读出来"""
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "ledger.json"
# Path(__file__) = 当前文件所在目录 → 数据文件固定放在包旁边，不会跟错路径

def load():
    """读文件。文件不存在就返回空列表"""
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save(records):
    """把记录列表整个写回文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)