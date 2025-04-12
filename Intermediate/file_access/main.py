with open("../../Data/newfile.txt") as file:
    content = file.read()
    #print(content)

with open("../../Data/newfile.txt", "a") as file:
    file.write("\nHello skibidi sigma")
