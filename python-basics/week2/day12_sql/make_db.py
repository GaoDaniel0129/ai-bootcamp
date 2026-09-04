import sqlite3

# 连接数据库文件；文件不存在会自动创建
conn = sqlite3.connect("shop.db")
cur = conn.cursor()      # cursor = 执行 SQL 的"手"

# 删旧表（保证脚本可重复运行；真实项目谨慎用 DROP）
cur.execute("DROP TABLE IF EXISTS orders")
cur.execute("DROP TABLE IF EXISTS users")

# 建 users 表
cur.execute("""
CREATE TABLE users (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,  -- 主键：每行唯一编号，自动增长
    name  TEXT    NOT NULL,
    city  TEXT    NOT NULL
)
""")

# 建 orders 表：user_id 指向 users.id —— 这就是"外键关系"
cur.execute("""
CREATE TABLE orders (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id  INTEGER NOT NULL,
    amount   REAL    NOT NULL,
    item     TEXT    NOT NULL
)
""")

# 插入示例数据（一次插多行）
cur.executemany("INSERT INTO users (name, city) VALUES (?, ?)",
                [("张三", "上海"), ("李四", "北京"), ("王五", "深圳")])
cur.executemany("INSERT INTO orders (user_id, amount, item) VALUES (?, ?, ?)",
                [(1, 199.0, "机械键盘"), (1, 39.9, "鼠标垫"),
                 (2, 5999.0, "显示器"), (3, 99.0, "数据线"), (3, 129.0, "充电器")])

conn.commit()   # ★ 提交事务：不写这行，改动不会真正保存
conn.close()
print("建表 + 插入完成")