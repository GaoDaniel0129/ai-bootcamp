from student import Student

s1 = Student("张三", 95)   # 创建对象 → 自动调用 __init__
s2 = Student("李四", 55)

print(s1.introduce())      # 调方法
print(s2.grade())          # 不及格
print(s1)                  # 触发 __str__
print([s1, s2])            # 列表里打印 → 触发 __repr__

"""
我叫张三，考了95分，优秀
不及格
Student(张三, 95)
[Student('张三', 95), Student('李四', 55)]
"""