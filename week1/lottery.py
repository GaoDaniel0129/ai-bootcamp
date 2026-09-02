import random

# 生成6个不重复的红球（1-33）
red_balls = random.sample(range(1, 34), 6)
red_balls.sort()  # 从小到大排序

# 生成1个蓝球（1-16）
blue_ball = random.randint(1, 16)

# 打印结果
print(f"红球: {red_balls}")
print(f"蓝球: {blue_ball}")
print(f"双色球号码: {red_balls} + {blue_ball}")

"""
红球: [2, 9, 17, 18, 20, 23]
蓝球: 13
双色球号码: [2, 9, 17, 18, 20, 23] + 13
"""