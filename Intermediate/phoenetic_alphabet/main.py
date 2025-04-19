student_dict = {
    "student": ["Angela", "James", "Lily"], 
    "score": [56, 76, 98]
}

#Looping through dictionaries:
for (key, value) in student_dict.items():
    #Access key and value
    pass

import pandas
student_data_frame = pandas.DataFrame(student_dict)

#Loop through rows of a data frame
for (index, row) in student_data_frame.iterrows():
    #Access index and row
    #Access row.student or row.score
    pass

# Keyword Method with iterrows()
# {new_key:new_value for (index, row) in df.iterrows()}

with open("nato_phonetic_alphabet.csv") as file:
    nato_data = pandas.read_csv(file)
    # print(nato_data)
#TODO 1. Create a dictionary in this format:
{"A": "Alfa", "B": "Bravo"}
phonetic_alphabet = {value.letter:value.code for key, value in nato_data.iterrows()}
print(phonetic_alphabet)
# print(phonetic_alphabet)
#TODO 2. Create a list of the phonetic code words from a word that the user inputs.
user_input = input("Enter a word: ").upper()
user_input_list = [letter for letter in list(user_input)]

phonetic_list = [phonetic_alphabet[letter] for letter in user_input_list if letter in phonetic_alphabet]
print(phonetic_list)
