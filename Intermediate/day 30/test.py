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

# height = float(input("Height: "))
# weight = int(input("Weight: "))

# if height > 3:
#     raise ValueError("Human height should not be over 3 meters.")
# bmi = weight / height ** 2
# print(bmi)

# my_dict = [{"name": "Pierre", "age": 30}, 
#            {"name": "Marie", "age": 25}, 
#            { "age": 27},
#            {"name": "Jean", "age": 40},
#            {"name": "Luc", "age": 22},
#            {"age": 35}]

# def print_name(list_of_names):
#     for name in list_of_names:
#         print(name["name"])

# try:
#     print_name(my_dict)
# except Exception as e:
#     print(f"no name in this dict")

# facebook_posts = [
#     {'Likes': 21, 'Comments': 2},
#     {'Likes': 13, 'Comments': 2, 'Shares': 1},
#     {'Likes': 33, 'Comments': 8, 'Shares': 3},
#     {'Comments': 4, 'Shares': 2},
#     {'Comments': 1, 'Shares': 1},
#     {'Likes': 19, 'Comments': 3}
# ]


# def count_likes(posts):

#     total_likes = 0
#     for post in posts:
#         try:
#             total_likes = total_likes + post['Likes']
#         except:
#             total_likes+=0
    
#     return total_likes


# print(count_likes(facebook_posts))

dict = {"names":{
            "peter":25,
            "mary": 60},
        "towns":{
            "kirchberg":452,
            "belval":360
        }}
#print(dict)

for i, j in dict.items():
    if i == "towns":
        for k,l in j.items():
            print(k,":",l)