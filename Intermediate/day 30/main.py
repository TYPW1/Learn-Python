# with open ("b_file.txt", "r") as file:
#     content = file.read()

# try:
#     file = open("b_file.txt")
#     a_dictionary = {"key": "value"}
#     print(a_dictionary["key"])
# except FileNotFoundError:
#     file = open("b_file.txt", "w")
# except KeyError as error_message:
#     print(f"The key {error_message} does not exist.")
# else:
#     content = file.read()
#     print(content)
# finally:
#     file.close()
#     print("File was closed.")

# while True:
#     try:
#         x = int(input("Please enter a number: "))
#         break
#     except ValueError:
#         print("Oops!  That was no valid number.  Try again...")

import pandas
data =pandas.read_csv("nato_phonetic_alphabet.csv")
phoenetic_dict = {row.letter:row.code for (index, row) in data.iterrows()}
print(phoenetic_dict)
word = input("Enter a word: ").upper()
output_list = [phoenetic_dict[letter] for letter in word]
print(output_list)