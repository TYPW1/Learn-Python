
dicti = [
    {"name": "peter",
     "age": 28,
     "city": "New York"}
]

for key in dicti[0]:
    if key == "city":
        print(dicti[0][key])
        print(key)