import json
import os

# 数据文件名
DATA_FILE = "grades.json"

# ============================================
# 数据读写函数
# ============================================
def load_grades():
    """加载成绩数据，文件不存在时返回空字典"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ 数据文件损坏，已初始化为空字典")
            return {}
    else:
        print("📄 成绩文件不存在，已创建新数据")
        return {}

def save_grades(grades):
    """保存成绩数据到文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(grades, f, ensure_ascii=False, indent=2)
    print("✅ 数据已保存")

# ============================================
# 核心功能函数
# ============================================
def add_grade(grades):
    """录入成绩（姓名+成绩）"""
    name = input("请输入学生姓名: ").strip()
    if not name:
        print("❌ 姓名不能为空！")
        return
    
    while True:
        score_input = input("请输入成绩: ")
        try:
            score = float(score_input)
            # 成绩范围检查（可选）
            if 0 <= score <= 100:
                grades[name] = score
                print(f"✅ 已录入 {name}: {score}分")
                break
            else:
                print("⚠️ 成绩应在 0-100 之间，请重新输入")
        except ValueError:
            print("❌ 请输入有效的数字成绩！")

def show_all(grades):
    """显示全部成绩"""
    if not grades:
        print("📭 暂无成绩数据")
        return
    
    print("\n" + "=" * 45)
    print(f"{'姓名':<15} {'成绩':>10} {'等级':>10}")
    print("-" * 45)
    
    for name, score in sorted(grades.items()):
        # 根据成绩评定等级
        if score >= 90:
            level = "A"
        elif score >= 80:
            level = "B"
        elif score >= 70:
            level = "C"
        elif score >= 60:
            level = "D"
        else:
            level = "F"
        
        print(f"{name:<15} {score:>10.1f} {level:>10}")
    
    print("-" * 45)
    print(f"共 {len(grades)} 名学生")
    print("=" * 45)

def calc_average(grades):
    """计算平均分"""
    if not grades:
        print("📭 暂无成绩数据，无法计算平均分")
        return
    
    total = sum(grades.values())
    count = len(grades)
    average = total / count
    
    # 找出最高分和最低分
    max_score = max(grades.values())
    min_score = min(grades.values())
    
    print("\n" + "=" * 40)
    print("          成绩统计")
    print("=" * 40)
    print(f"学生人数: {count}")
    print(f"总分: {total:.1f}")
    print(f"平均分: {average:.2f}")
    print(f"最高分: {max_score:.1f}")
    print(f"最低分: {min_score:.1f}")
    
    # 及格率
    passed = sum(1 for s in grades.values() if s >= 60)
    pass_rate = (passed / count) * 100
    print(f"及格人数: {passed}/{count} ({pass_rate:.1f}%)")
    print("=" * 40)

# ============================================
# 主菜单
# ============================================
def display_menu():
    print("\n" + "=" * 40)
    print("       📚 学生成绩管理系统")
    print("=" * 40)
    print("1. 录入成绩")
    print("2. 显示全部成绩")
    print("3. 统计成绩（平均分/最高分/及格率）")
    print("0. 退出系统")
    print("=" * 40)

# ============================================
# 主程序
# ============================================
def main():
    # 启动时加载数据
    grades = load_grades()
    print(f"📊 当前共有 {len(grades)} 条成绩记录")
    
    while True:
        display_menu()
        choice = input("请选择操作 (0-3): ").strip()
        
        if choice == "1":
            add_grade(grades)
            save_grades(grades)  # 每次修改后保存
        
        elif choice == "2":
            show_all(grades)
        
        elif choice == "3":
            calc_average(grades)
        
        elif choice == "0":
            print("👋 感谢使用成绩管理系统！再见！")
            break
        
        else:
            print("❌ 无效选择，请重新输入 (0-3)")

# 程序入口
if __name__ == "__main__":
    main()

"""
📄 成绩文件不存在，已创建新数据
📊 当前共有 0 条成绩记录

========================================
       📚 学生成绩管理系统
========================================
1. 录入成绩
2. 显示全部成绩
3. 统计成绩（平均分/最高分/及格率）
0. 退出系统
========================================
请选择操作 (0-3): 1
请输入学生姓名: zhangsan
请输入成绩: 80
✅ 已录入 zhangsan: 80.0分
✅ 数据已保存

========================================
       📚 学生成绩管理系统
========================================
1. 录入成绩
2. 显示全部成绩
3. 统计成绩（平均分/最高分/及格率）
0. 退出系统
========================================
请选择操作 (0-3): 2

=============================================
姓名                      成绩         等级
---------------------------------------------
zhangsan              80.0          B
---------------------------------------------
共 1 名学生
=============================================

========================================
       📚 学生成绩管理系统
========================================
1. 录入成绩
2. 显示全部成绩
3. 统计成绩（平均分/最高分/及格率）
0. 退出系统
========================================
请选择操作 (0-3): 3

========================================
          成绩统计
========================================
学生人数: 1
总分: 80.0
平均分: 80.00
最高分: 80.0
最低分: 80.0
及格人数: 1/1 (100.0%)
========================================

========================================
       📚 学生成绩管理系统
========================================
1. 录入成绩
2. 显示全部成绩
3. 统计成绩（平均分/最高分/及格率）
0. 退出系统
========================================
请选择操作 (0-3): 0
👋 感谢使用成绩管理系统！再见！
"""