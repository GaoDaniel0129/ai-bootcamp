"""tools.py：Agent 的工具注册表 + 分发器"""
import ast
import operator
import datetime

# ---- 工具1：天气（演示用内置表，保证确定性；真实项目换成天气 API 即可）----
_WEATHER = {
    "上海":   {"today": "多云 26°C",  "tomorrow": "小雨 18°C"},
    "北京":   {"today": "晴 22°C",    "tomorrow": "晴 24°C"},
    "深圳":   {"today": "阵雨 28°C",  "tomorrow": "大雨 25°C"},
}

def get_weather(city: str, day: str = "today") -> dict:
    """查询城市天气。day 取 today 或 tomorrow"""
    city = city.strip()
    if city not in _WEATHER:
        return {"error": f"没有 {city} 的天气数据，可选：{list(_WEATHER)}"}
    info = _WEATHER[city].get(day)
    if info is None:
        return {"error": "day 参数只能取 today 或 tomorrow"}
    return {"city": city, "day": day, "weather": info}

# ---- 工具2：安全计算器（用 ast 白名单，绝不 eval 裸字符串）----
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv}

def _safe_eval(node):
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    raise ValueError("只支持 + - * / 和数字")

def calculator(expression: str) -> dict:
    """计算四则运算表达式，如 '15*(7-2)+10'"""
    try:
        return {"result": _safe_eval(ast.parse(expression, mode="eval"))}
    except Exception as e:
        return {"error": f"表达式无法计算：{e}"}

# ---- 工具注册表：名字 -> (函数, 描述) ----
TOOLS = [
    {"type": "function", "function": {
        "name": "get_weather",
        "description": "查询城市当天或次日的天气。参数 city 为城市名，day 为 today 或 tomorrow",
        "parameters": {"type": "object",
                       "properties": {"city": {"type": "string"},
                                      "day": {"type": "string", "enum": ["today", "tomorrow"]}},
                       "required": ["city"]}}},
    {"type": "function", "function": {
        "name": "calculator",
        "description": "计算数学表达式，支持 + - * / 和括号，如 15*(7-2)+10",
        "parameters": {"type": "object",
                       "properties": {"expression": {"type": "string"}},
                       "required": ["expression"]}}},
]

def dispatch(name: str, args: dict):
    """按名字执行工具。返回的一定是能 json.dumps 的 dict/str/list"""
    if name == "get_weather":
        return get_weather(**args)
    if name == "calculator":
        return calculator(**args)
    return {"error": f"未知工具：{name}"}