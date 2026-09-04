def make_multiplier(factor):
    """造一个"乘以 factor"的函数"""
    def multiply(x):
        return x * factor   # 内层函数用了外层变量 factor
    return multiply         # 把内层函数作为返回值递出去 → 形成闭包

double = make_multiplier(2)   # double 是一个函数
triple = make_multiplier(3)
print(double(10))   # 20
print(triple(10))   # 30

print("-" * 40)

import time

def timer(func):
    """装饰器：给函数加"打印耗时"能力"""
    def wrapper(*args, **kwargs):
        start = time.perf_counter()          # 调用前：记开始时间
        result = func(*args, **kwargs)       # 调用原函数（*args/**kwargs 接收任意参数）
        cost = time.perf_counter() - start   # 调用后：算耗时
        print(f"[{func.__name__}] 耗时 {cost:.4f} 秒")
        return result                        # 原函数的返回值必须原样返回！
    return wrapper

@timer                        # 语法糖，等价于 slow_add = timer(slow_add)
def slow_add(a, b):
    time.sleep(1)             # 模拟慢操作
    return a + b

print("结果：", slow_add(3, 4))

"""
[slow_add] 耗时 1.0005 秒
结果： 7
"""

print("-" * 40)

import time

def repeat(times):
    """带参数的装饰器：让函数重复执行 times 次"""
    def decorator(func):          # 第二层：接收原函数
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator              # 第三层：返回真正的装饰器

@repeat(3)                        # 先执行 repeat(3) → decorator → 套到 say_hi 上
def say_hi():
    print("你好")

say_hi()

"""
你好
你好
你好
"""

print("-" * 40)

def fib():
    """斐波那契生成器：无限序列，但每次只产出一个数"""
    a, b = 0, 1
    while True:          # 无限循环也不怕——因为每次只算一步
        yield a          # yield = "先给一个数出去，下次从这行继续"
        a, b = b, a + b

f = fib()                # 注意：调用不执行函数体！只是创建生成器
print(next(f))           # 0   → next() 推进一步
print(next(f))           # 1
print(next(f))           # 1
print(next(f))           # 2
print(next(f))           # 3

"""
0
1
1
2
3
"""

print("-" * 40)

# 用法一：for 直接消费（最常用）
for i, num in enumerate(fib()):
    if i >= 8:
        break
    print(num, end=" ")
print()

# 用法二：大文件逐行读（10GB 日志也不怕——内存里永远只有一行）
def read_big_file(path):
    """一次 yield 一行，内存占用 O(1)"""
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()

for line in read_big_file("ledger.json"):
    if "ERROR" in line:
        print(line)   # 10GB 文件里筛 ERROR 行，内存几乎不涨
        break

# 用法三：生成器表达式（把推导式的 [] 换成 () 就是生成器）
squares = (x * x for x in range(1000000))   # 几乎不占内存
print(sum(squares)) 

"""
0 1 1 2 3 5 8 13 
333332833333500000
"""