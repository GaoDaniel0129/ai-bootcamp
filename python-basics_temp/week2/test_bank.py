from bank import BankAccount

acc = BankAccount("Daniel", 100)
print(acc)
acc.deposit(500)
print(acc)
acc.withdraw(200)
print(acc)

# 故意触发异常，练习 try/except 接住业务错误
try:
    acc.withdraw(99999)
except ValueError as e:
    print("取款被拒绝：", e)

print("账户操作记录：", acc.transactions)

"""
账户[Daniel] 余额：100 元
账户[Daniel] 余额：600 元
账户[Daniel] 余额：400 元
取款被拒绝： 余额不足：当前余额 400，想取 99999
账户操作记录： ['存入 500', '取出 200']
"""