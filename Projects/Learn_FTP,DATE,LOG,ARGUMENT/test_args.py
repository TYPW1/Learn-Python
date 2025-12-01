# Basic argparse practice
import argparse

# 1. Create the parser
p = argparse.ArgumentParser()

# 2. Tell it which arguments to look for
p.add_argument("--start", required=True, type=int)
p.add_argument("--end", required=True, type=int)

# 3. Read the command line and get the values
args = p.parse_args()

# 4. Use the values
print(f"Starting from: {args.start}")
print(f"Ending at: {args.end}")

print(f"Type of start: {type(args.start)}")
print(f"Type of end: {type(args.end)}")

# Now we can do math!
difference = args.end - args.start
print(f"The difference is: {difference}")