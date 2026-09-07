"""main.py：命令行多轮对话机器人（含工具）"""
import json
import sys
import llm
from tools import TOOL_MAP

SYSTEM_PROMPT = ("你是 Daniel 的 AI 助手。需要实时数据或计算时调用工具，"
                 "根据工具结果用中文简洁回答。")

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

def run_turn(user_input):
    messages.append({"role": "user", "content": user_input})
    for _ in range(5):                      # 工具循环上限 5 次
        resp = llm.chat(messages)
        text, tool_calls = llm.parse_stream(resp)

        if not tool_calls:
            if text:
                messages.append({"role": "assistant", "content": text})
            return

        # 有工具调用：把模型请求先入历史，再回传工具结果
        messages.append({"role": "assistant",
                         "content": text or None,
                         "tool_calls": [{
                             "id": tc["id"],
                             "type": "function",
                             "function": {"name": tc["name"],
                                          "arguments": tc["args"]}}
                             for tc in tool_calls]})
        for tc in tool_calls:
            print(f"  ⚙ 调用工具 {tc['name']} ...")
            result = TOOL_MAP[tc["name"]](
                **json.loads(tc["args"]))
            print(f"  ✔ 结果：{result}")
            messages.append({"role": "tool",
                             "tool_call_id": tc["id"],
                             "content": str(result)})

print("🤖 多轮对话机器人就绪（流式 + 工具）")
print("   试试：上海天气怎么样 / 帮我算 12*13+7")
print("   指令：/clear 清空历史 · exit 退出")
while True:
    try:
        user_input = input("\n你> ").strip()
    except (KeyboardInterrupt, EOFError):
        break
    if user_input in ("exit", "quit"):
        break
    if user_input == "/clear":
        messages[:] = [{"role": "system", "content": SYSTEM_PROMPT}]
        print("历史已清空")
        continue
    if user_input:
        try:
            run_turn(user_input)
        except Exception as e:
            print(f"\n⚠ 出错：{e}。这一轮已跳过，历史已清理，请重试。")
            # 清理：撤掉刚才的 user 消息和可能残留的 assistant/tool
            while messages and messages[-1]["role"] != "system":
                messages.pop()

"""
🤖 多轮对话机器人就绪（流式 + 工具）                                      
   试试：上海天气怎么样 / 帮我算 12*13+7
   指令：/clear 清空历史 · exit 退出

你> 你好，我叫丹尼尔
你好，丹尼尔！很高兴认识你。😊

我是你的 AI 助手，可以帮你处理各种任务，比如：

- **查询天气**：告诉我城市名，我帮你查当前天气
- **数学计算**：提供算式，我帮你计算
- **其他问题**：有任何疑问都可以问我

有什么我可以帮你的吗？

你> 我叫什么？
你叫**丹尼尔**呀！😊 刚才你告诉我的，我记得很清楚。

有什么需要我帮忙的吗？

你> 上海天气怎么样？
我来帮你查询一下上海的天气。
  ⚙ 调用工具 get_weather ...
  ✔ 结果：上海：晴，31℃
丹尼尔，上海现在的天气情况如下：

🌤️ **上海天气**
- **天气状况**：晴
- **气温**：31℃

天气晴朗，气温较高，出门记得注意防晒、多补充水分哦！还有什么需要帮忙的吗？

你> 帮我算 (123+456)*78
我来帮你计算这个算式。
  ⚙ 调用工具 calculator ...
  ✔ 结果：(123+456)*78 = 45162
丹尼尔，计算结果如下：

**(123 + 456) × 78 = 45162**

计算过程：
- 先算括号内：123 + 456 = 579
- 再乘以 78：579 × 78 = 45162

还有其他需要帮忙的吗？😊

你> /clear
历史已清空

你> 我叫什么？
抱歉，我并不知道您的名字。您还没有告诉我您的名字呢。请问您叫什么名字？😊

你> exit
"""