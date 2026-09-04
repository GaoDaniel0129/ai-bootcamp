# 字典 = 按键取值，像查字典一样快
stu = {"name": "Daniel", "age": 25, "city": "上海"}
print(stu["name"])        # 按键取值
print(stu.get("salary"))  # 键不存在返回 None，不报错

stu["job"] = "developer"  # 新增键
stu["age"] = 26           # 修改已有键
print(stu)

# 遍历：.items() 同时拿键和值
for k, v in stu.items():
    print(k, "→", v)

# 判断键是否存在
if "city" in stu:
    print("city 存在")

"""
Daniel
None
{'name': 'Daniel', 'age': 26, 'city': '上海', 'job': 'developer'}
name → Daniel
age → 26
city → 上海
job → developer
city 存在
"""

print("--------------------")

# 需求：统计一句话里每个词出现几次
text = "the cat and the dog and the bird"
words = text.split(" ")          # 按空格切成词列表
count = {}                       # 空字典，词→次数
for w in words:
    count[w] = count.get(w, 0) + 1   # 关键一行：取不到就给 0
print(count)

"""
{'the': 3, 'cat': 1, 'and': 2, 'dog': 1, 'bird': 1}
"""

print("--------------------")

# 集合 = 无序的不重复元素
tags_a = {"python", "ai", "linux"}
tags_b = {"python", "docker"}

print(tags_a & tags_b)    # 交集（& 是 and 符号）
print(tags_a | tags_b)    # 并集
print(tags_a - tags_b)    # 差集：a 有 b 没有

# 最常用场景：列表去重
names = ["张三", "李四", "张三", "王五"]
print(list(set(names)))   # 转集合自动去重，再转回列表

"""
{'python'}
{'linux', 'docker', 'ai', 'python'}
{'linux', 'ai'}
['李四', '张三', '王五']
"""