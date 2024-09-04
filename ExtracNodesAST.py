import ast
import json
from os.path import join
from pathlib import Path

code = """
def calculate_circle_area(radius):
    return math.pi * radius ** 2

def calculate_circle_circumference(radius):
    return 2 * math.pi * radius

radius = 7
print("Area:", calculate_circle_area(radius))
# print("Circumference:", calculate_circle_circumference(radius))
"""
DEFAULT_OUTPUT_FILE = join(Path(__file__).parent, 'output.json')


def parse(codes):
    return ast.parse(codes)


class Visitor(ast.NodeVisitor):
    def __init__(self):
        self.operators = []

    def visit_BinOp(self, node):
        # Capture binary operations (e.g., +, -, *, /)
        self.operators.append({
            "operator_type": type(node.op).__name__,
            "lineno": node.lineno
        })
        self.generic_visit(node)

    def visit_UnaryOp(self, node):
        # Capture unary operations (e.g., -, not)
        self.operators.append({
            "operator_type": type(node.op).__name__,
            "lineno": node.lineno
        })
        self.generic_visit(node)

    def visit_BoolOp(self, node):

        self.operators.append({
            "operator_type": type(node.op).__name__,
            "lineno": node.lineno
        })
        self.generic_visit(node)

    def visit_Compare(self, node):
        # Capture comparison operations (e.g., ==, >, <)
        for op in node.ops:
            self.operators.append({
                "operator_type": type(op).__name__,
                "lineno": node.lineno
            })
        self.generic_visit(node)


def extract_function_def(tree):
    visitor = Visitor()
    visitor.visit(tree)
    return visitor


def parse_code(codes, output_file):
    tree = parse(codes)
    functions = extract_function_def(tree)

    file_info = {
        "functions": []
    }

    for function in tree.body:
        if isinstance(function, ast.FunctionDef):
            operator_visitor = Visitor()
            operator_visitor.visit(function)

            function_info = {
                "function name": function.name,
                "operators": operator_visitor.operators
            }

            file_info["functions"].append(function_info)

    with open(output_file, 'w') as outfile:
        json.dump(file_info, outfile, indent=4)
    print(f"Results exported to {output_file}")


parse_code(code, DEFAULT_OUTPUT_FILE)
