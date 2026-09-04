# 变量 = 给数据起名字
age = 25              # 整数 int
price = 9.9           # 浮点 float（小数）
name = "Daniel"       # 字符串 str（必须用引号）

print(age)
print(type(age))      # type() 看类型
print(type(price))
print(type(name))

"""
25
<class 'int'>
<class 'float'>
<class 'str'>
"""


# 字符串"25" 和 数字 25 是两回事
s = "25"
print(s + "岁")        # 字符串拼接，OK
print(int(s) + 1)     # int() 转成数字，结果是 26

# 下面这行会报错，先看报错，再注释掉
# print(s + 1)        # TypeError: 字符串和数字不能相加

"""
25岁
26

25岁
26
Traceback (most recent call last):
  File "D:\ai-bootcamp\week1\day1_intro.py", line 24, in <module>
    print(s + 1)        # TypeError: 字符串和数字不能相加
          ~~^~~
TypeError: can only concatenate str (not "int") to str
"""


name = "Daniel"
age = 25
print(f"我叫{name}，今年{age}岁")
# 结果：我叫Daniel，今年25岁
# f 表示 format，大括号{}里放变量，会自动替换成值

"""
我叫Daniel，今年25岁
"""


# input() 会等你在终端打字，回车确认
your_name = input("请输入你的名字：")
print(f"你好，{your_name}！欢迎开始学 Python")

# input 得到的一定是字符串，要算数必须先转
birth_year = input("请输入出生年份：")
age = 2026 - int(birth_year)      # int() 转换
print(f"你今年大约{age}岁")

"""
请输入你的名字：gaoyuan
你好，gaoyuan！欢迎开始学 Python
请输入出生年份：1995
你今年大约31岁
"""