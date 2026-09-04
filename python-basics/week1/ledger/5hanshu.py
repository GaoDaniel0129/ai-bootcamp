# ============================================
# 1. max3(a, b, c)：返回三个数中最大的
# ============================================
def max3(a, b, c):
    """返回三个数中最大的（不使用内置max函数）"""
    if a >= b and a >= c:
        return a
    elif b >= a and b >= c:
        return b
    else:
        return c

# ============================================
# 2. is_prime(n)：判断是否为素数
# ============================================
def is_prime(n):
    """判断一个数是否为素数，返回True/False"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # 检查奇数因子到平方根
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

# ============================================
# 3. fib(n)：返回第n个斐波那契数
# ============================================
def fib(n):
    """返回第n个斐波那契数（0,1,1,2,3,5,8,...）"""
    if n < 0:
        return None
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    a, b = 0, 1
    for i in range(2, n + 1):
        a, b = b, a + b
    return b

# ============================================
# 4. avg(lst)：返回列表平均值
# ============================================
def avg(lst):
    """返回列表的平均值"""
    if not lst:  # 空列表处理
        return 0
    total = 0
    for num in lst:
        total += num
    return total / len(lst)

# ============================================
# 5. 用 lambda + sorted 给单词按长度排序
# ============================================
def sort_by_length(words):
    """用lambda + sorted按单词长度排序"""
    return sorted(words, key=lambda x: len(x))

# ============================================
# 测试所有函数
# ============================================
print("=" * 50)
print("          函数测试")
print("=" * 50)

# 测试1: max3
print("\n【测试 max3】")
print(f"max3(5, 3, 8) = {max3(5, 3, 8)}")
print(f"max3(10, 10, 7) = {max3(10, 10, 7)}")
print(f"max3(-1, -5, -3) = {max3(-1, -5, -3)}")

# 测试2: is_prime
print("\n【测试 is_prime】")
test_nums = [2, 3, 4, 17, 25, 37, 100, 1]
for num in test_nums:
    print(f"is_prime({num}) = {is_prime(num)}")

# 测试3: fib
print("\n【测试 fib】")
print(f"fib(0) = {fib(0)}")
print(f"fib(1) = {fib(1)}")
print(f"fib(2) = {fib(2)}")
print(f"fib(5) = {fib(5)}")
print(f"fib(10) = {fib(10)}")
# 显示前10个斐波那契数列
fib_sequence = [fib(i) for i in range(10)]
print(f"前10个斐波那契数: {fib_sequence}")

# 测试4: avg
print("\n【测试 avg】")
print(f"avg([10, 20, 30, 40, 50]) = {avg([10, 20, 30, 40, 50])}")
print(f"avg([5, 7, 9]) = {avg([5, 7, 9])}")
print(f"avg([]) = {avg([])}")  # 空列表

# 测试5: 按长度排序
print("\n【测试 按长度排序】")
words = ["apple", "I", "programming", "is", "Python", "fun", "language"]
sorted_words = sort_by_length(words)
print(f"原始列表: {words}")
print(f"按长度排序: {sorted_words}")

# 使用sorted直接测试（带key）
print("\n【直接使用 lambda 示例】")
test_words = ["hello", "a", "world", "python", "hi", "code"]
sorted_by_len = sorted(test_words, key=lambda x: len(x))
print(f"原始: {test_words}")
print(f"按长度排序: {sorted_by_len}")
# 降序排列
sorted_by_len_desc = sorted(test_words, key=lambda x: len(x), reverse=True)
print(f"按长度降序: {sorted_by_len_desc}")

print("\n" + "=" * 50)
print("          全部测试完成！")
print("=" * 50)

"""
==================================================
          函数测试
==================================================

【测试 max3】
max3(5, 3, 8) = 8
max3(10, 10, 7) = 10
max3(-1, -5, -3) = -1

【测试 is_prime】
is_prime(2) = True
is_prime(3) = True
is_prime(4) = False
is_prime(17) = True
is_prime(25) = False
is_prime(37) = True
is_prime(100) = False
is_prime(1) = False

【测试 fib】
fib(0) = 0
fib(1) = 1
fib(2) = 1
fib(5) = 5
fib(10) = 55
前10个斐波那契数: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

【测试 avg】
avg([10, 20, 30, 40, 50]) = 30.0
avg([5, 7, 9]) = 7.0
avg([]) = 0

【测试 按长度排序】
原始列表: ['apple', 'I', 'programming', 'is', 'Python', 'fun', 'language']
按长度排序: ['I', 'is', 'fun', 'apple', 'Python', 'language', 'programming']

【直接使用 lambda 示例】
原始: ['hello', 'a', 'world', 'python', 'hi', 'code']
按长度排序: ['a', 'hi', 'code', 'hello', 'world', 'python']
按长度降序: ['python', 'hello', 'world', 'code', 'hi', 'a']

==================================================
          全部测试完成！
==================================================
"""