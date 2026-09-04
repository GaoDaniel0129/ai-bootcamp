print("JOIN 查询")

import sqlite3
conn = sqlite3.connect("shop.db")
cur = conn.cursor()

cur.execute("""
SELECT u.name, COUNT(o.id) AS 订单数, SUM(o.amount) AS 总金额
FROM users u                     -- u 是 users 的别名
LEFT JOIN orders o ON o.user_id = u.id   -- 按"外键=主键"配对
GROUP BY u.id                   -- 按用户分组后统计
ORDER BY 总金额 DESC
""")
for name, cnt, total in cur.fetchall():
    print(f"{name:>4}  订单 {cnt} 笔  共 {total} 元")
conn.close()

"""
JOIN 查询
  李四  订单 1 笔  共 5999.0 元
  张三  订单 2 笔  共 238.9 元
  王五  订单 2 笔  共 228.0 元
"""