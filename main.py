#Password Generator Project
import random
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("Welcome to the PyPassword Generator!")
nr_letters= int(input("How many letters would you like in your password?\n"))
nr_symbols = int(input(f"How many symbols would you like?\n"))
nr_numbers = int(input(f"How many numbers would you like?\n"))

#Eazy Level - Order not randomised:
#e.g. 4 letter, 2 symbol, 2 number = JduE&!91
test = random.randint(0,len(letters))
#for n in range (0, len(letters+1)):
#  letters[n] =
lpass = []
for nr_letters in range (1, nr_letters+1):
  lpass.append(letters[random.randint(0,len(letters)-1)])
print (lpass)

spass = []
for nr_symbols in range (1, nr_symbols+1):
   spass.append(symbols[random.randint(0,len(symbols)-1)])
print (spass)

npass = []
for nr_numbers in range (1, nr_numbers+1):
   npass.append(numbers[random.randint(0,len(numbers)-1)])
print (npass)

password = []
password.extend(lpass+npass+spass)

final = 0
i = (random.sample(password,len(password)))
for j in i:
    print(j, end=" ")


#Hard Level - Order of characters randomised:
#e.g. 4 letter, 2 symbol, 2 number = g^2jk8&P