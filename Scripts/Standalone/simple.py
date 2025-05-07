def ret_num(target, arr):
    dict_num = {}
    for  num in arr:
        if num in dict_num:
            dict_num[num] = arr.index(num)