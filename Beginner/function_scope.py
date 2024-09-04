import ast
import json
from os.path import join
from pathlib import Path



'''
class FunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = []

    def visit_ClassDef(self, nodes):
        # print(f"Function name: {node.name}")
        # print(ast.dump(node, indent=4, include_attributes=True))
        self.functions.append(nodes)
        self.generic_visit(nodes)


def parse(codes):
    return ast.parse(codes)


def extract_node(tree):

    visitor = FunctionVisitor()
    visitor.visit(tree)
    return visitor.functions


# print(extract_node(parse(code)))

functions = []
for node in extract_node(parse(code)):
    print(ast.dump(node, indent=4, include_attributes=True))
'''

DEFAULT_OUTPUT_FILE = join(Path(__file__).parent, 'results.json')


class ExpressionsVisitor(ast.NodeVisitor):
    def __init__(self):
        self.expressions = []

    def visit_FunctionDef(self, node):
        self.expressions.append(node)
        self.generic_visit(node)


def parse(codes):
    return ast.parse(codes)


def extract_expressions(tree):
    visitor = ExpressionsVisitor()
    visitor.visit(tree)
    return visitor.expressions

# Function to convert AST node to a dictionary
def node_to_dict(node):
    # If the node is an AST object, convert it to a dictionary
    if isinstance(node, ast.AST):
        fields = {key: node_to_dict(value) for key, value in ast.iter_fields(node)}
        attributes = {key: getattr(node, key) for key in node._attributes if hasattr(node, key)}
        return {
            'type': node.__class__.__name__,
            **fields,
            **attributes
        }
    # If it's a list, convert each item
    elif isinstance(node, list):
        return [node_to_dict(item) for item in node]
    # Otherwise, return the node's value
    else:
        return node

code = """
def divide(a, b):
    try:
        result = a / b
        result = a / b
        result = a / b
    except ZeroDivisionError:
        return "Cannot divide by zero"
    return result

print("Division result:", divide(10, 2))
print("Division result:", divide(10, 0))

"""

nodes = extract_expressions(parse(code))

dumped_nodes = [node_to_dict(node) for node in nodes]

for node in extract_expressions(parse(code)):
    print(ast.dump(node, indent=4, include_attributes=True))

with open(DEFAULT_OUTPUT_FILE, 'w') as outfile:
    json.dump(dumped_nodes, outfile, indent=4)