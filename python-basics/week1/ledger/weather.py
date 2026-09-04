import requests

# 请求天气数据（format=j1 返回JSON格式）
url = "https://wttr.in/Shanghai?format=j1"
resp = requests.get(url, timeout=10)  # 10秒超时
data = resp.json()  # 将响应转换为字典

# 从JSON中提取当前天气信息
cur = data["current_condition"][0]  # 取第一个当前天气对象
temp = cur["temp_C"]  # 温度（摄氏）
desc = cur["weatherDesc"][0]["value"]  # 天气描述（嵌套在列表中）
humidity = cur["humidity"]  # 湿度

# 打印天气信息
print(f"上海当前：{temp}°C，{desc}，湿度 {humidity}%")

"""
上海当前：30°C，Patchy rain nearby，湿度 67%
"""