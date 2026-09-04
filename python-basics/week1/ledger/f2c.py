# 输入华氏温度
fahrenheit = float(input("请输入华氏温度: "))

# 计算摄氏温度
celsius = (fahrenheit - 32) * 5 / 9

# 输出结果（保留两位小数）
print(f"摄氏温度为: {celsius:.2f}°C")

"""
请输入华氏温度: 30
摄氏温度为: -1.11°C
"""