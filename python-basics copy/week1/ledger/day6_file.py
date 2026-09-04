# w = 写入（覆盖旧内容）；a = 追加；r = 读取
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")

# 重新读回来
with open("notes.txt", "r", encoding="utf-8") as f:
    content = f.read()
print(content)
print("--- 按行读 ---")
with open("notes.txt", "r", encoding="utf-8") as f:
    for line in f:            # 文件对象可直接迭代
        print("读到:", line.strip())

print("--------------------------")

import json

data = {"name": "Daniel", "skills": ["python", "linux"], "age": 26}

# dict → JSON 字符串（dump 到文件 / dumps 到字符串）
with open("profile.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# JSON 文件 → dict
with open("profile.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
print(loaded["name"])
print(loaded["skills"][0])

"""
Daniel
python
"""

print("--------------------------")

try:
    num = int(input("输入一个数字："))
    print("100 / 它 =", 100 / num)
except ValueError:
    print("那不是数字！")
except ZeroDivisionError:
    print("不能除以 0！")
else:
    print("没出错才执行这里")
finally:
    print("无论对错都执行这里（关文件/收尾用）")

"""
输入一个数字：50
100 / 它 = 2.0
没出错才执行这里
无论对错都执行这里（关文件/收尾用）
"""