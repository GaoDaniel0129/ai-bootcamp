class BankAccount:
    """银行账户：存钱、取钱、查余额"""

    def __init__(self, owner, balance=0):
        if balance < 0:
            raise ValueError("开户余额不能为负")
        self.owner = owner
        self.balance = balance
        self.transactions = []      # 每笔操作的记录

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("存款金额必须大于 0")
        self.balance += amount
        self.transactions.append(f"存入 {amount}")
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("取款金额必须大于 0")
        if amount > self.balance:
            # 业务规则：余额不足 → 抛异常，让调用方决定怎么处理
            raise ValueError(f"余额不足：当前余额 {self.balance}，想取 {amount}")
        self.balance -= amount
        self.transactions.append(f"取出 {amount}")
        return self.balance

    def __str__(self):
        return f"账户[{self.owner}] 余额：{self.balance} 元"