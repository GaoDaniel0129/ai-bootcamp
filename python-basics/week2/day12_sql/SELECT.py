print("==查询==")

import sqlite3
conn = sqlite3.connect("shop.db")
cur = conn.cursor()

# ① 全查 + 排序 + 限量
cur.execute("SELECT name, city FROM users ORDER BY id DESC LIMIT 2")
for row in cur.fetchall():          # fetchall = 拿全部结果（每行是元组）
    print(row)                      # ('王五','深圳') ('李四','北京')

# ② WHERE 过滤
cur.execute("SELECT item, amount FROM orders WHERE amount >= 100")
for row in cur.fetchall():
    print(row)                      # ('机械键盘',199.0) ('显示器',5999.0)

# ③ 统计函数
cur.execute("SELECT COUNT(*), SUM(amount) FROM orders")
print(cur.fetchone())               # (5, 6465.8)  fetchone = 只拿第一行

# ④ 模糊查询（今天 Day 14 通讯录的 search 就靠它）
cur.execute("SELECT name FROM users WHERE name LIKE '%张%'")
print(cur.fetchall())               # [('张三',)]
conn.close()

"""
==查询==
('王五', '深圳')
('李四', '北京')
('机械键盘', 199.0)
('显示器', 5999.0)
('充电器', 129.0)
(5, 6465.9)
[('张三',)]
"""