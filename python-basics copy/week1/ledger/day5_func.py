def greet(name, age=18):      # age 有默认值，可以不传
    """返回一句问候语"""       # 函数说明（docstring）
    return f"你好 {name}，{age} 岁"

print(greet("Daniel"))         # 用默认 age
print(greet("Alice", 30))      # 位置参数
print(greet(age=25, name="Bob"))  # 关键字参数，顺序可换

"""
你好 Daniel，18 岁
你好 Alice，30 岁
你好 Bob，25 岁
"""

print("" + "-" * 20 + "\n")

def add_print(a, b):
    print(a + b)          # 只打印，不返回

def add_return(a, b):
    return a + b          # 只返回，不打印

r1 = add_print(1, 2)      # 打印了 3
r2 = add_return(1, 2)     # 什么都不打印
print("r1 =", r1)         # r1 是 None！
print("r2 =", r2)         # r2 是 3

"""

3
r1 = None
r2 = 3
"""

print("" + "-" * 20 + "\n")

count = 0                 # 全局变量

def add_one():
    global count          # 声明"我要改的是全局那个"
    count += 1

add_one()
add_one()
print(count)              # 2

# 不加 global 会怎样？试试：
def try_change():
    count = 99            # 这是函数自己的局部变量，和全局无关
try_change()
print(count)              # 还是 2

"""
2
2
"""

print("" + "-" * 20 + "\n")

# 普通写法
def double(x):
    return x * 2
# lambda 写法（只能写一行表达式）
double2 = lambda x: x * 2
print(double(5), double2(5))      # 10 10

# lambda 真正用途：给排序当"钥匙"
names = ["Daniel", "bob", "alice"]
names.sort(key=lambda s: len(s))  # 按名字长度排
print(names)
names.sort(key=lambda s: s.lower())  # 按字母序（忽略大小写）
print(names)

"""
10 10
['bob', 'alice', 'Daniel']
['alice', 'bob', 'Daniel']
"""