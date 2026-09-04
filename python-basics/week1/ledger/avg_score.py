# 输入5个成绩
scores = []
for i in range(5):
    score = float(input(f"请输入第{i+1}个成绩: "))
    scores.append(score)

# 计算平均分和最高分
average = sum(scores) / len(scores)
max_score = max(scores)

# 输出结果
print(f"成绩列表: {scores}")
print(f"平均分: {average:.2f}")
print(f"最高分: {max_score}")

"""
请输入第1个成绩: 80
请输入第2个成绩: 90
请输入第3个成绩: 100
请输入第4个成绩: 60
请输入第5个成绩: 50
成绩列表: [80.0, 90.0, 100.0, 60.0, 50.0]
平均分: 76.00
最高分: 100.0
"""