import ast
import json

class CustomNodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.variables = []

    def visit_Name(self, node):
        self.variables.append({
            "id": node.id,  # The name of the variable as a string
            "lineno": node.lineno,  # The line number as an integer
            "col_offset": node.col_offset  # The column offset as an integer
        })
        self.generic_visit(node)

def parse_elements(file_path):
    with open(file_path, "r") as source:
        tree = ast.parse(source.read(), filename=file_path)
    visitor = CustomNodeVisitor()
    visitor.visit(tree)
    return {
        "variables": visitor.variables
    }

# Example usage:
file_path = "Beginner/test.py"  # Replace with your Python file
elements = parse_elements(file_path)
print(json.dumps(elements, indent=4))
