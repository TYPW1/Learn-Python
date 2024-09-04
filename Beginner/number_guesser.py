import random


def check_guess(attempts):
    number = random.randint(1, 100)
    while attempts > 0:
        guesses = int(input("Enter number\n"))
        if guesses == number:
            print("You WIN")
            break
        else:
            if attempts > 0:
                attempts -= 1
                print(f"{attempts} more chances")
                if guesses > number:
                    print("Your number is higher")
                else:
                    print("your number is lower")
            else:
                print("No more guesses")


difficulty = input("choose difficulty\n")

if difficulty == "hard":
    attempt = 5
    check_guess(attempt)
else:
    attempt = 10
    check_guess(attempt)
