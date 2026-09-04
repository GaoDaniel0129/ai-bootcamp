import sqlite3
conn = sqlite3.connect("shop.db")
cur = conn.cursor()

# UPDATE：改（忘写 WHERE = 改全表！）
cur.execute("UPDATE users SET city = '杭州' WHERE name = '张三'")
print("受影响行数：", cur.rowcount)      # 1

# DELETE：删（忘写 WHERE = 清空全表！）
cur.execute("DELETE FROM orders WHERE amount < 50")
print("删除行数：", cur.rowcount)         # 1（鼠标垫 39.9 被删）

conn.commit()
conn.close()

"""
受影响行数： 1
删除行数： 1
"""