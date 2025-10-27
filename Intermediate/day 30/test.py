# class B(Exception):
#     pass

# class C(B):
#     pass

# class D(C):
#     pass

# for cls in [B, C, D]:
#     try:
#         raise cls()
#     except D:
#         print("D")
#     except C:
#         print("C")
#     except B:
#         print("B")

height = float(input("Height: "))
weight = int(input("Weight: "))

if height > 3:
    raise ValueError("Human height should not be over 3 meters.")
bmi = weight / height ** 2
print(bmi)