"""main.py：命令行记账（简易版）"""
import sys
import storage   # 同包模块，直接 import 模块名

def add(amount, note):
    records = storage.load()
    records.append({"amount": float(amount), "note": note})
    storage.save(records)
    print(f"已记录：{amount} 元 —— {note}")

def show():
    records = storage.load()
    if not records:
        print("暂无记录")
        return
    total = sum(r["amount"] for r in records)
    for r in records:
        print(f"{r['amount']:>10}  {r['note']}")
    print(f"{'合计':>10}  {total}")

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "add" and len(sys.argv) == 4:
        add(sys.argv[2], sys.argv[3])
    elif cmd == "show":
        show()
    else:
        print("用法：python main.py add 金额 备注   或   python main.py show")

if __name__ == "__main__":
    main()