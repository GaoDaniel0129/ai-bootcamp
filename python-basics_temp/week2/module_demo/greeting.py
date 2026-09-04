"""打招呼模块：只做一件事——根据时间返回问候语"""

def morning():
    return "早上好，开工！"

def evening():
    return "晚上好，复盘时间。"

def greet(name):
    import datetime
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        msg = "早上好"
    elif 12 <= hour < 18:
        msg = "下午好"
    else:
        msg = "晚上好"
    return f"{msg}，{name}！"

# print("我被执行了！")

def main():
    """直接运行时执行的入口"""
    print(greeting_demo_test())   # 只是演示，可替换成真测试

def greeting_demo_test():
    return "greeting 模块自检通过"

if __name__ == "__main__":
    main()   # 只有直接运行本文件时才执行