import ast

def parse_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    tree = ast.parse(code)
    return ast.dump(tree, indent=4)

# Example usage
file_path = 'example.py'
parsed_file = parse_file(file_path)
print(parsed_file)
