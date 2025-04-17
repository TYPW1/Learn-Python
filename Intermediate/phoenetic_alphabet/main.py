# numbers = [1, 2, 3, 4, 5]
# new_list = [n+1 for n in numbers]
# print(new_list)
# # Output: [2, 3, 4, 5, 6]

# name = "Pieere"

# letters = [letter for letter in name]
# print(letters)

# number = [n+n for n in range(1, 6)]
# print(number)

names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy", "Kevin", "Laura", "Mallory", "Nina", "Oscar", "Peggy", "Quentin", "Rupert", "Sybil", "Trent", "Uma", "Victor", "Walter", "Xena", "Yara", "Zane"]
short_names = [name for name in names if len(name) <= 2]

long_names_caps = [name.upper() for name in names if len(name) > 5]
