import sys
import json
import os
import datetime

DATA_FILE = "ledger.json"

# ============================================
# 数据读写函数
# ============================================
def load():
    """返回记录列表；文件不存在返回[]"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ 数据文件损坏，已初始化为空列表")
            return []
    return []

def save(records):
    """把 records 写回 DATA_FILE"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

# ============================================
# 辅助函数：计算净额
# ============================================
def calc_net(records):
    """计算净额（收入 - 支出）"""
    total = 0
    for r in records:
        if r["type"] == "income":
            total += r["amount"]
        else:
            total -= r["amount"]
    return total

# ============================================
# 命令处理函数
# ============================================
def cmd_add():
    """添加记录：add 金额 备注 [收入]"""
    records = load()
    
    try:
        amount = float(sys.argv[2])
    except ValueError:
        print("❌ 金额必须是数字")
        return
    except IndexError:
        print("❌ 请指定金额")
        return
    
    try:
        note = sys.argv[3]
    except IndexError:
        print("❌ 请填写备注")
        return
    
    # 判断类型：第4个参数是"收入"则为收入，否则为支出
    if len(sys.argv) > 4 and sys.argv[4] == "收入":
        kind = "income"
        tag = "收入"
    else:
        kind = "expense"
        tag = "支出"
    
    # 生成今天日期
    today = datetime.date.today().isoformat()  # 2026-09-03
    
    # 添加记录
    records.append({
        "amount": amount,
        "note": note,
        "type": kind,
        "date": today
    })
    
    save(records)
    print(f"✅ 已记录：{tag} {amount}元 {note}")

def cmd_list():
    """列出全部记录"""
    records = load()
    if not records:
        print("📭 暂无记录")
        return
    
    print("\n" + "-" * 50)
    print(f"{'日期':<12} {'类型':<6} {'金额':>8} {'备注'}")
    print("-" * 50)
    
    for r in records:
        tag = "收入" if r["type"] == "income" else "支出"
        print(f"{r['date']:<12} {tag:<6} {r['amount']:>8.2f} {r['note']}")
    
    print("-" * 50)
    print(f"共 {len(records)} 条记录")
    
    # 显示净额
    net = calc_net(records)
    print(f"净额: {net:.2f}元")
    print("-" * 50)

def cmd_total():
    """汇总净额（收入 - 支出）"""
    records = load()
    if not records:
        print("📭 暂无记录，净额为 0")
        return
    
    net = calc_net(records)
    print(f"净额：{net:.2f}元")

def cmd_month():
    """查看某月的记录和净额"""
    try:
        month = sys.argv[2]
    except IndexError:
        print("❌ 请指定月份，例如: python ledger.py month 9")
        return
    
    # 补零：9 → "09"
    month_str = month.zfill(2)
    
    # 过滤出该月的记录
    records = load()
    month_records = [
        r for r in records 
        if r["date"].startswith(f"2026-{month_str}")
    ]
    
    if not month_records:
        print(f"📭 {month}月 暂无记录")
        return
    
    # 显示记录
    print(f"\n📅 {month}月 账单")
    print("-" * 50)
    print(f"{'日期':<12} {'类型':<6} {'金额':>8} {'备注'}")
    print("-" * 50)
    
    for r in month_records:
        tag = "收入" if r["type"] == "income" else "支出"
        print(f"{r['date']:<12} {tag:<6} {r['amount']:>8.2f} {r['note']}")
    
    print("-" * 50)
    print(f"共 {len(month_records)} 条记录")
    
    # 计算并显示净额
    net = calc_net(month_records)
    print(f"净额: {net:.2f}元")
    print("-" * 50)

def show_usage():
    """显示用法提示"""
    print("""
📊 命令行记账工具

用法:
  python ledger.py add 金额 备注         # 记录一笔支出
  python ledger.py add 金额 备注 收入    # 记录一笔收入
  python ledger.py list                  # 列出全部记录
  python ledger.py total                 # 汇总净额
  python ledger.py month 月份            # 查看某月记录

示例:
  python ledger.py add 30 午餐
  python ledger.py add 1000 工资 收入
  python ledger.py list
  python ledger.py total
  python ledger.py month 9
""")

# ============================================
# 主程序
# ============================================
def main():
    if len(sys.argv) < 2:
        show_usage()
        return
    
    cmd = sys.argv[1]
    
    if cmd == "add":
        cmd_add()
    elif cmd == "list":
        cmd_list()
    elif cmd == "total":
        cmd_total()
    elif cmd == "month":
        cmd_month()
    elif cmd == "help" or cmd == "-h" or cmd == "--help":
        show_usage()
    else:
        print(f"❌ 未知命令: {cmd}")
        print("使用 'python ledger.py help' 查看帮助")

if __name__ == "__main__":
    main()

"""
(.venv) PS D:\ai-bootcamp> python .\week1\ledger.py


  python ledger.py add 金额 备注         # 记录一笔支出
  python ledger.py list                  # 列出全部记录
  python ledger.py month 月份            # 查看某月记录

示例:
  python ledger.py add 30 午餐
  python ledger.py add 1000 工资 收入
  python ledger.py list
  python ledger.py total
  python ledger.py month 9

(.venv) PS D:\ai-bootcamp> python .\week1\ledger.py list
(.venv) PS D:\ai-bootcamp> python .\week1\ledger.py add 30 午餐
(.venv) PS D:\ai-bootcamp> python .\week1\ledger.py add 1000 工资 收入
✅ 已记录：收入 1000.0元 工资
(.venv) PS D:\ai-bootcamp> python .\week1\ledger.py list              

--------------------------------------------------
日期           类型           金额 备注
--------------------------------------------------
2026-09-03   支出        30.00 午餐
2026-09-03   收入      1000.00 工资
--------------------------------------------------
共 2 条记录
净额: 970.00元
--------------------------------------------------
(.venv) PS D:\ai-bootcamp> python .\week1\ledger.py total             
净额：970.00元
(.venv) PS D:\ai-bootcamp> python .\week1\ledger.py month 9

📅 9月 账单
--------------------------------------------------
日期           类型           金额 备注
--------------------------------------------------
2026-09-03   支出        30.00 午餐
2026-09-03   收入      1000.00 工资
--------------------------------------------------
共 2 条记录
净额: 970.00元
--------------------------------------------------
"""