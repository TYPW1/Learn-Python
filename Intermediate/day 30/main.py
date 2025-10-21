# with open ("b_file.txt", "r") as file:
#     content = file.read()

try:
    file = open("b_file.txt")
except  FileNotFoundError:
    print("An error occurred while trying to open the file.")
else:
    print("correct File found")

# while True:
#     try:
#         x = int(input("Please enter a number: "))
#         break
#     except ValueError:
#         print("Oops!  That was no valid number.  Try again...")