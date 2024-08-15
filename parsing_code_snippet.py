import ast

def parse_code(code):
    tree = ast.parse(code)
    return ast.dump(tree, indent=4)

# Example usage
code = """
def hello_world():
    print("Hello, world!")
"""
parsed_code = parse_code(code)
print(parsed_code)
