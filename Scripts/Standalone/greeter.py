import argparse

def main():
    """The main function of our script."""
    print("Script is running")

    #create parser
    parser = argparse.ArgumentParser(description=" A Script that greets you")

    #add arguments
    parser.add_argument('name', help="The name of the person to greet")

    #add optional arguments
    parser.add_argument('--greeting', help="The greeting to use", default="Hello")

    #add a flag argument
    parser.add_argument('--verbose', help="Enable verbose mode.", action = 'store_true')

    #parse arguments
    args = parser.parse_args()

    #we use flag with an if statement
    if args.verbose:
        print("Verbose mode is ON.")
        print(F"Preparing to greet {args.name}...")
    #Use the arguments
    print(f"{args.greeting}, {args.name}")

    if args.verbose:
        print("Greeting complete.")
if __name__ == "__main__":
    main()