def add(n1, n2):
    return n1 + n2

def subtract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    if n2 != 0:
        return n1 / n2
    else:
        return "Error! Division by zero."

operations = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}

while True:  # Start an infinite loop to keep the calculator running
    no1 = int(input("What's the first number?: "))
    print("+\n-\n*\n/")
    operation = input("Pick an operation: ")
    no2 = int(input("What's the second number?: "))

    result = operations[operation](no1, no2)
    print(f"{no1} {operation} {no2} = {result}")

    choice = input(f"Type 'y' to continue calculating with {result}, or type 'n' to start a new calculation, or 'q' to quit: ").lower()

    if choice == "y":
        operation = input("Pick an operation: ")
        no3 = int(input("What's the next number?: "))
        final_result = operations[operation](result, no3)
        print(f"{result} {operation} {no3} = {final_result}")
    elif choice == "n":
        continue  # This will start a new calculation
    elif choice == "q":
        print("Goodbye!")
        break  # Exit the loop and end the program
    else:
        print("Invalid input, exiting.")
        break  # Exit the loop if the input is not recognized
