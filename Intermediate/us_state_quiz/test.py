name = "peter willy"
p = name.title()
#print(p)
import random
names = ["peter", "willy", "john", "doe", "jane", "smith", "alice", "bob"]
student_scores={student:random.randint(1,100) for student in names}

passed_students = {student:score for student,score in student_scores.items() if score > 50}

for name in passed_students.keys():
    print(name)