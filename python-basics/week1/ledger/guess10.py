import random

# 生成随机数字 (1-100)
secret = random.randint(1, 100)
max_attempts = 10
attempts = 0

print("🎯 猜数字游戏开始！")
print(f"我已经想好了一个 1-100 之间的数字，你有 {max_attempts} 次机会！")
print("-" * 40)

while True:
    # 输入猜测
    guess = int(input(f"第 {attempts + 1} 次猜测: "))
    attempts += 1
    
    # 判断大小
    if guess < secret:
        print("📈 太小了，再大一点！")
    elif guess > secret:
        print("📉 太大了，再小一点！")
    else:
        print(f"🎉 恭喜你猜对了！答案是 {secret}")
        print(f"你用了 {attempts} 次机会")
        break
    
    # 检查是否达到最大次数
    if attempts >= max_attempts:
        print(f"❌ 失败！答案是 {secret}")
        print(f"你已经用完了 {max_attempts} 次机会")
        break

print("游戏结束！")

"""
🎯 猜数字游戏开始！
我已经想好了一个 1-100 之间的数字，你有 10 次机会！
----------------------------------------
第 1 次猜测: 50
📉 太大了，再小一点！
第 2 次猜测: 25
📉 太大了，再小一点！
第 3 次猜测: 12
📉 太大了，再小一点！
第 4 次猜测: 6
🎉 恭喜你猜对了！答案是 6
你用了 4 次机会
游戏结束！
"""