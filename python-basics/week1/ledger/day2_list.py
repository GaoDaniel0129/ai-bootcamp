# 列表 = 有序的箱子，可以放任意数据，可以改
fruits = ["苹果", "香蕉", "橘子"]
print(fruits[0])        # 下标从 0 开始 → 苹果
print(fruits[-1])       # -1 是倒数第一个 → 橘子
print(fruits[1:])       # 从下标 1 到最后 → ['香蕉', '橘子']

fruits.append("葡萄")   # 末尾追加
fruits.insert(1, "梨")  # 插到下标 1
fruits.remove("香蕉")   # 按值删除（没有会报错）
last = fruits.pop()     # 弹出最后一个并返回
print(fruits)
print("弹出了", last)
print("长度", len(fruits))

'''
苹果
橘子
['香蕉', '橘子']
['苹果', '梨', '橘子']
弹出了 葡萄
长度 3
'''

print("=====================================")

nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(nums[1:5])     # 下标1到4 → 含1不含5（左闭右开）
print(nums[:3])      # 开头省略 = 从0开始
print(nums[5:])      # 结尾省略 = 到最后
print(nums[::2])     # 步长2，隔一个取一个
print(nums[::-1])    # 步长-1 = 反转整张表

"""
[1, 2, 3, 4]
[0, 1, 2]
[5, 6, 7, 8, 9]
[0, 2, 4, 6, 8]
[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
"""

print("=====================================")

# 元组 = 不可变的列表，用来存"不该被改"的数据
point = (10, 20)
print(point[0])        # 10
# point[0] = 99        # 取消注释会报错：元组不能改

# 元组解包：一次取出所有值
x, y = point
print("x =", x, "y =", y)

# 用途举例：坐标、日期、函数的多个返回值
def get_min_max(nums):
    return min(nums), max(nums)   # 返回元组
lo, hi = get_min_max([3, 1, 4, 1, 5])
print(lo, hi)

"""
10
x = 10 y = 20
1 5
"""