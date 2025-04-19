name = "peter willy"
p = name.title()
#print(p)
import random
names = ["peter", "willy", "john", "doe", "jane", "smith", "alice", "bob"]
student_scores={student:random.randint(1,100) for student in names}

passed_students = {student:score for student,score in student_scores.items() if score > 50}

import pandas as pd

student_dict = {
    "student": ["Angela", "james", "Lily"],
    "score": [56,76,98]
}

#normal loop through dictionary
for key,value in student_dict.items():
    print("")

#create a data frame from the dictionary
student_data_frame = pd.DataFrame(student_dict)



#loop through the data frame via items
for key, value in student_data_frame.items():
    print("")

#loop through the dataframe via iterrows
for index, row in student_data_frame.iterrows():
    # print(row.student)
    # print(row.score)
    # print(row["student"])
    # print(row["score"])
    if row.student == "james":
        print(row.score)