"""react.py：手写 ReAct 循环（今天的高潮，逐行读懂它）"""
import json
import os
from openai import OpenAI
from tools import TOOLS, dispatch

client = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"],
                base_url="https://api.deepseek.com/v1")

SYSTEM = ("你是一个会调用工具的助手。每次先输出 Thought（中文，简短说明你要做什么），"
          "然后调用工具。看到工具结果后继续推理，直到信息足够，再输出 Final Answer 给用户。")

def run_agent(user_query: str, max_steps: int = 6) -> None:
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": user_query}]
    for step in range(1, max_steps + 1):
        print(f"---- 第 {step} 轮 ----")
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",      # 让模型自己决定调不调
            temperature=0.2)         # 工具调用场景温度调低，减少乱来
        msg = resp.choices[0].message

        # 模型既说话又要求调工具：它的文字一般是 Thought，先打印
        if msg.content:
            print("[模型] " + msg.content[:200])

        if not msg.tool_calls:       # 不再要工具 = 该收尾了
            print("[完成] " + (msg.content or "(无内容)"))
            return

        # 把 assistant 这条带 tool_calls 的消息原样放回历史（协议要求）
        messages.append(msg)
        for tc in msg.tool_calls:
            name, args = tc.function.name, json.loads(tc.function.arguments or "{}")
            print(f"[调用工具] {name}({args})")
            result = dispatch(name, args)
            # tool 消息必须带 tool_call_id 与 assistant 里的对上
            messages.append({"role": "tool", "tool_call_id": tc.id,
                             "content": json.dumps(result, ensure_ascii=False)})
    print("[强制结束] 达到最大步数，防止死循环")

if __name__ == "__main__":
    run_agent("上海明天会下雨吗？我出门要不要带伞？如果带伞，帮我算一下买 3 把 15.5 元的伞总共多少钱。")

"""
---- 第 1 轮 ----
[模型] I'll check Shanghai's weather for tomorrow first.
[调用工具] get_weather({'city': '上海', 'day': 'tomorrow'})
---- 第 2 轮 ----
[模型] 上海明天有小雨，需要带伞。现在算一下 3 把伞的总价。
[调用工具] calculator({'expression': '3*15.5'})
---- 第 3 轮 ----
[模型] **上海明天天气：小雨，18°C** —— 会下雨，建议带伞出门。

如果买 3 把 15.5 元的伞，总共 **46.5 元**。
[完成] **上海明天天气：小雨，18°C** —— 会下雨，建议带伞出门。

如果买 3 把 15.5 元的伞，总共 **46.5 元**。
"""