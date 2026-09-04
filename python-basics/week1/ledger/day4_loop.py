score = int(input("输入成绩："))
if score >= 90:
    grade = "A"
elif score >= 60:      # elif = else if
    grade = "B"
else:
    grade = "C"
print(f"等级：{grade}")

# 逻辑运算：and or not
if 0 <= score <= 100:
    print("成绩合法")
if score < 0 or score > 100:
    print("成绩不合法")

"""
输入成绩：100
等级：A
成绩合法

输入成绩：60
等级：B
成绩合法

输入成绩：30
等级：C
成绩合法

输入成绩：-100
等级：C
成绩不合法
"""

print("-" * 40)

# range(5) = 0,1,2,3,4 （不含 5）
for i in range(5):
    print(i, end=" ")     # end=" " 表示用空格结尾不换行
print()                   # 补一个换行

# 1 加到 100
total = 0
for n in range(1, 101):   # 1 到 100（含 100）
    total += n            # total = total + n 的简写
print("1加到100 =", total)

# enumerate：循环时同时拿下标和值
names = ["张三", "李四"]
for idx, name in enumerate(names):
    print(idx, name)

"""
0 1 2 3 4 
1加到100 = 5050
0 张三
1 李四
"""

print("-" * 40)

import random
secret = random.randint(1, 100)   # 随机 1-100
tries = 0
while True:                       # 无限循环，靠 break 退出
    guess = int(input("猜一个 1-100 的数："))
    tries += 1
    if guess > secret:
        print("大了")
    elif guess < secret:
        print("小了")
    else:
        print(f"猜对了！用了 {tries} 次")
        break                     # 退出循环

"""
猜一个 1-100 的数：55
小了
猜一个 1-100 的数：40
小了
猜一个 1-100 的数：80
小了
猜一个 1-100 的数：90
大了
猜一个 1-100 的数：88
猜对了！用了 5 次
"""