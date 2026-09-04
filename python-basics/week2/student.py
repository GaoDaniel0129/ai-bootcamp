class Student:
    """学生类：每个学生有名字和分数"""

    def __init__(self, name, score):
        """构造函数：创建对象时自动执行，用来给属性赋初值"""
        self.name = name      # self 指"将来创建出来的那个对象本身"
        self.score = score

    def grade(self):
        """方法：计算成绩等级"""
        if self.score >= 90:
            return "优秀"
        elif self.score >= 60:
            return "及格"
        return "不及格"

    def introduce(self):
        return f"我叫{self.name}，考了{self.score}分，{self.grade()}"

    def __str__(self):
        """print(对象) 时显示什么（给人看的）"""
        return f"Student({self.name}, {self.score})"

    def __repr__(self):
        """调试时显示什么（给开发者看的），约定尽量能还原代码"""
        return f"Student('{self.name}', {self.score})"