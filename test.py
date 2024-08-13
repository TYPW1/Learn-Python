test = {
    "a": 5,
    "b": 9,
    "c": 12,
    "d": 6
}

keep ={}
for item in test:
    if test[item] == 12:
        keep[item] = 55

    if test[item] >= 6 and test[item] <= 9:
        keep[item] = 8

print (keep)