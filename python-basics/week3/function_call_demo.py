"""function_call_demo.py：Function Calling 完整流程"""
import json
import os
import requests

API_KEY = os.environ["DEEPSEEK_API_KEY"]
URL = "https://api.deepseek.com/chat/completions"

# —— 工具定义（20.2 的 tools）和真函数（20.3）粘贴到这里 ——
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",                    # 函数名，必须和你的真函数对应
            "description": "查询指定城市当前天气，输入城市名（中文），返回温度和天气状况",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名，如 上海、北京"
                    }
                },
                "required": ["city"]                   # 必填参数列表
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "执行四则运算。需要表达式字符串，如 '12*8' 或 '100/7'",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "算术表达式，只支持 + - * / 和括号"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# 伪数据版天气（真实 API 接入放 W7 项目3）
def get_weather(city):
    fake_db = {"上海": ("晴", 31), "北京": ("多云", 26), "深圳": ("阵雨", 29)}
    if city not in fake_db:
        return f"没有 {city} 的天气数据"
    cond, temp = fake_db[city]
    return f"{city}：{cond}，{temp}℃"

def calculator(expression):
    # 只允许白名单字符，防止 eval 注入（绝不直接 eval 用户输入！）
    if not all(c in "0123456789+-*/(). " for c in expression):
        return "表达式含非法字符"
    try:
        return f"{expression} = {eval(expression, {'__builtins__': {}}, {})}"
    except Exception as e:
        return f"计算失败：{e}"

# 工具名 → 真函数 的路由表
TOOL_MAP = {"get_weather": get_weather, "calculator": calculator}


def call_llm(messages, tools=None):
    payload = {"model": "deepseek-chat", "messages": messages,
               "temperature": 0, "stream": False}
    if tools:
        payload["tools"] = tools
    resp = requests.post(URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json=payload, timeout=60)
    return resp.json()["choices"][0]["message"]

# 主流程：可能需要多轮（模型可能一次调多个工具）
def run(user_question):
    messages = [
        {"role": "system",
         "content": "你是智能助手。需要实时数据或计算时调用工具，根据工具结果用中文回答。"},
        {"role": "user", "content": user_question},
    ]
    for _ in range(5):                       # 最多 5 轮工具循环，防死循环
        msg = call_llm(messages, tools)
        messages.append(msg)                 # 模型这轮的回复进历史

        # 情况 A：模型想调用工具
        if msg.get("tool_calls"):
            for tc in msg["tool_calls"]:
                fn_name = tc["function"]["name"]
                args = json.loads(tc["function"]["arguments"])
                print(f"→ 模型决定调用：{fn_name}({args})")
                result = TOOL_MAP[fn_name](**args)
                print(f"→ 工具返回：{result}")
                # 把工具结果作为 tool 角色的消息回传（必须一一对应 id）
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "content": str(result),
                })
            continue                          # 带着工具结果再问一次模型

        # 情况 B：模型直接给了最终回答
        return msg["content"]

print(run("上海今天天气怎么样？"))
print("---")
print(run("帮我算 (123+456)*78 等于多少"))

"""
→ 模型决定调用：get_weather({'city': '上海'})                  
→ 工具返回：上海：晴，31℃
根据查询结果，上海今天的天气情况如下：

🌤️ **上海今日天气**
- **天气状况**：晴
- **气温**：31℃

今天上海天气晴朗，气温较高，比较炎热。建议您注意防晒、多补充水分，外出时做好防暑降温措施哦！如果需要了解其他城市或更多信息，随时告诉我。
---
→ 模型决定调用：calculator({'expression': '(123+456)*78'})
→ 工具返回：(123+456)*78 = 45162
计算结果如下：

**(123 + 456) × 78 = 45162**

计算过程：
- 先算括号内：123 + 456 = 579
- 再乘以 78：579 × 78 = 45162

所以答案是 **45162**。
"""