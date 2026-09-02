# 找出 1-100 的所有素数
primes = []

for num in range(2, 101):  # 从2开始，1不是素数
    is_prime = True
    
    # 试除：从2到num-1
    for i in range(2, num):
        if num % i == 0:  # 能被整除，不是素数
            is_prime = False
            break  # 找到因子就可以退出
    
    if is_prime:
        primes.append(num)

print("1-100 的素数有:")
print(primes)
print(f"共有 {len(primes)} 个素数")

"""
1-100 的素数有:
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
共有 25 个素数
"""