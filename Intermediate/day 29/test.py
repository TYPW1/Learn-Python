for i in range (3, 10):
    pass

num = [i for i in range(3, 10)]  # generator expression
print(num)  # <generator object <genexpr> at 0x000001E

num = []
for i in range (3, 10):
    num.append(i)   
print(num)  # [3, 4, 5, 6, 7, 8, 9]