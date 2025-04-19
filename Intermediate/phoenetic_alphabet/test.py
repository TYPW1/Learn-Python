import pandas as pd

classroom = {"names": ["Angela", "James", "Lily"],
            "scores": [56, 76, 98],
            "grades": ["A", "B", "C"],
            "age": [20, 21, 22],}
classroom_dataframe = pd.DataFrame(classroom)

# for (index, value) in classroom_dataframe.iterrows():
#     print(value.names)
#     print(value.scores)

name = "peter"
print(list(name))