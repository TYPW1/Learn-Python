# import csv
# with open ("weather_data.csv") as data_file:
#     data = csv.reader(data_file)
#     temperature = []
#     for row in data:
#         if row[1] != "temp":
#             temperature.append(int(row[1]))
#

import pandas
data = pandas.read_csv("weather_data.csv")
#print(data["temp"])
temp_list = data["temp"].to_list()

average = sum(temp_list)/(len(temp_list))

avr = data["temp"].mean()

max = data["temp"].max()

min = data.temp.min()

data[data.day == "Monday"]

data[data .temp == data.temp.max()]

monday = data[data.day == "Monday"]
temp_conv = monday.temp * 9/5 + 32

data_dict = {
    "student": ["Angela", "James", "Luna"],
    "score": [56, 76, 98]
}

data = pandas.DataFrame(data_dict)

data.to_csv("new_data.csv")

