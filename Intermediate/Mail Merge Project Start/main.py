#TODO: Create a letter using starting_letter.txt 
#for each name in invited_names.txt
#Replace the [name] placeholder with the actual name.
#Save the letters in the folder "ReadyToSend".
from operator import index

#Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
    #Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
        #Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp

with open("./Input/Letters/starting_letter.txt", "r") as template:
    line_content = template.readlines()

with open("./Input/Names/invited_names.txt", "r") as names:
    names_content = names.readlines()


for name in names_content:
    name = name.strip()
    with open(f"./Output/ReadyToSend/{name}.txt", "w") as final:
        new_Content = line_content
        modified_content = new_Content[0].replace("[name]", name)
        last = ''.join(new_Content[1:])
        first = modified_content
        final.write(first + last)

