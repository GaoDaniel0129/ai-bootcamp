"""tools.py：工具定义与实现"""
import json

def get_weather(city):
    fake_db = {"上海": ("晴", 31), "北京": ("多云", 26), "深圳": ("阵雨", 29)}
    if city not in fake_db:
        return f"没有 {city} 的天气数据"
    cond, temp = fake_db[city]
    return f"{city}：{cond}，{temp}℃"

def calculator(expression):
    if not all(c in "0123456789+-*/(). " for c in expression):
        return "表达式含非法字符"
    try:
        return f"{expression} = {eval(expression, {'__builtins__': {}}, {})}"
    except Exception as e:
        return f"计算失败：{e}"

TOOLS = [
    {"type": "function", "function": {
        "name": "get_weather",
        "description": "查询指定城市当前天气，输入中文城市名",
        "parameters": {"type": "object",
                       "properties": {"city": {"type": "string", "description": "城市名"}},
                       "required": ["city"]}}},
    {"type": "function", "function": {
        "name": "calculator",
        "description": "四则运算，输入表达式如 (123+456)*78",
        "parameters": {"type": "object",
                       "properties": {"expression": {"type": "string", "description": "算术表达式"}},
                       "required": ["expression"]}}},
]

TOOL_MAP = {"get_weather": get_weather, "calculator": calculator}

def run_tool(name, args_json):
    """执行工具：name=工具名，args_json=模型给的参数字符串"""
    args = json.loads(args_json)
    return TOOL_MAP[name](**args)