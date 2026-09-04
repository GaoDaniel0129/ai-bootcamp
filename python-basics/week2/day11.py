# 传统写法
result = []
for i in range(10):
    if i % 2 == 0:
        result.append(i * 10)
print(result)

# 推导式写法（一行搞定）
result2 = [i * 10 for i in range(10) if i % 2 == 0]
print(result2)

"""
[0, 20, 40, 60, 80]
[0, 20, 40, 60, 80]
"""

names = ["张三", "李四", "王五"]
# 字典推导式：名字 → 名字长度
d = {n: len(n) for n in names}
print(d)                    # {'张三': 2, '李四': 2, '王五': 2}

# 集合推导式：自动去重
words = ["a", "b", "a", "c", "b"]
print({w.upper() for w in words})   # {'A', 'B', 'C'}（顺序不保证）

"""
{'张三': 2, '李四': 2, '王五': 2}
{'C', 'B', 'A'}
"""

# map：把函数作用到每个元素上 → 新迭代器
nums = [1, 2, 3, 4]
print(list(map(lambda x: x ** 2, nums)))    # [1, 4, 9, 16]（配合 lambda 匿名函数）
# 注：lambda x: x**2 = 一句写完的迷你函数

# filter：按条件过滤
print(list(filter(lambda x: x % 2 == 0, nums)))   # [2, 4]

# sorted：排序，key 指定按什么排
students = [("张三", 95), ("李四", 55), ("王五", 88)]
by_score = sorted(students, key=lambda s: s[1], reverse=True)
print(by_score)   # [('张三', 95), ('王五', 88), ('李四', 55)]

# enumerate：遍历时同时拿到"第几个"
for idx, name in enumerate(names, start=1):
    print(f"第{idx}名：{name}")

# zip：把多个列表按位置"拉链"合并
scores = [95, 55, 88]
print(list(zip(names, scores)))   # [('张三', 95), ('李四', 55), ('王五', 88)]

"""
[1, 4, 9, 16]
[2, 4]
[('张三', 95), ('王五', 88), ('李四', 55)]
第1名：张三
第2名：李四
第3名：王五
[('张三', 95), ('李四', 55), ('王五', 88)]
"""

from collections import Counter, deque, defaultdict

# ① Counter：统计出现次数（最常用）
text = "python python java python go go rust"
word_counts = Counter(text.split())
print(word_counts)                 # Counter({'python': 3, 'go': 2, ...})
print(word_counts.most_common(2))  # 出现最多的 2 个：直接返回 [('python',3),('go',2)]

# ② deque：双端队列，左右都能快速增删（滑动窗口/队列）
from collections import deque
dq = deque([1, 2, 3])
dq.append(4)        # 右边加
dq.appendleft(0)    # 左边加
print(list(dq))     # [0, 1, 2, 3, 4]
dq.popleft()        # 左边出
print(list(dq))     # [1, 2, 3, 4]

# ③ defaultdict：字典取值时"没有就自动给默认值"，告别 KeyError
d = defaultdict(list)        # 默认值类型是空列表
d["数学"].append(90)          # 键不存在也直接能用！
d["数学"].append(85)
d["英语"].append(88)
print(dict(d))               # {'数学': [90, 85], '英语': [88]}

"""
Counter({'python': 3, 'go': 2, 'java': 1, 'rust': 1})
[('python', 3), ('go', 2)]
[0, 1, 2, 3, 4]
[1, 2, 3, 4]
{'数学': [90, 85], '英语': [88]}
"""

import datetime

now = datetime.datetime.now()
print(now)                          # 2026-09-08 15:30:00.123456（实际时间）
print(now.strftime("%Y-%m-%d %H:%M"))   # 格式化：2026-09-08 15:30
print(now.date())                   # 只要日期：2026-09-08
print(now.weekday())                # 星期几（0=周一）

# 字符串 → datetime（解析用户输入/接口返回的时间）
s = "2026-09-08 15:30:00"
dt = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")   # 格式必须和字符串一一对应
print(dt.year, dt.month)            # 2026 9

# 时间加减
tomorrow = now + datetime.timedelta(days=1)
print(tomorrow.date())              # 明天

"""
2026-09-04 14:06:28.006575
2026-09-04 14:06
2026-09-04
4
2026 9
2026-09-05
"""

from collections import Counter

text = """the quick brown fox jumps over the lazy dog the fox the dog
python is great python is fast python is fun"""
# 清洗：统一小写 + 只保留字母（用推导式过滤）
words = [w.lower() for w in text.split() if w.isalpha()]

# 统计：Counter 一行
top5 = Counter(words).most_common(5)
for word, cnt in top5:
    print(f"{word:>10} 出现 {cnt} 次")

"""
       the 出现 4 次
    python 出现 3 次
        is 出现 3 次
       fox 出现 2 次
       dog 出现 2 次
"""