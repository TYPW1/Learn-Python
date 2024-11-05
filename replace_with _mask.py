import copy
import re
from fileinput import lineno
import json
import ast
import astpretty
import astor
#from caffe2.python.transformations_test import transformer

code ="""class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


def ring(self):
    return 2 * (self.width + self.height)

rect = Rectangle(10, 5)
radius = 7 * 5
print("Area:", rect.area())
print("Perimeter:", rect.perimeter())
"""

json_file_with_mask = """{
    "masked_binops": [
        {
            "left": "self.width * self.height",
            "op": "<mask>",
            "right": "self.height",
            "lineno": 7,
            "col_offset": 15,
            "end_col_offset": 53,
            "original": "*"
        },
        {
            "left": "self.width",
            "op": "<mask>",
            "right": "self.height",
            "lineno": 7,
            "col_offset": 15,
            "end_col_offset": 39,
            "original": "*"
        },
        {
            "left": "2",
            "op": "<mask>",
            "right": "self.width + self.height",
            "lineno": 10,
            "col_offset": 15,
            "end_col_offset": 45,
            "original": "*"
        },
        {
            "left": "self.width",
            "op": "<mask>",
            "right": "self.height",
            "lineno": 10,
            "col_offset": 20,
            "end_col_offset": 44,
            "original": "+"
        },
        {
            "left": "2",
            "op": "<mask>",
            "right": "self.width + self.height",
            "lineno": 14,
            "col_offset": 11,
            "end_col_offset": 41,
            "original": "*"
        },
        {
            "left": "self.width",
            "op": "<mask>",
            "right": "self.height",
            "lineno": 14,
            "col_offset": 16,
            "end_col_offset": 40,
            "original": "+"
        },
        {
            "left": "7",
            "op": "<mask>",
            "right": "5",
            "lineno": 18,
            "col_offset": 9,
            "end_col_offset": 14,
            "original": "*"
        }
    ],
    "masked_boolops": [],
    "masked_unaryops": [],
    "masked_compares": [],
    "masked_global_binops": [
        {
            "left": "7",
            "op": "<mask>",
            "right": "5",
            "lineno": 18,
            "col_offset": 9,
            "end_col_offset": 14,
            "original": "*"
        }
    ],
    "masked_global_boolops": [],
    "masked_global_unaryops": [],
    "masked_global_compares": []
}"""


MASK ="<mask>"
# Parsing JSON string into a Python dictionary
masked_versions = json.loads(json_file_with_mask)

def parse_code_to_ast(codes):
    return ast.parse(codes)


def unparse_ast_to_code(trees):
    return ast.unparse(trees)

tree = parse_code_to_ast(code)
#print("Tree:",ast.dump(tree,indent=4, include_attributes=True))
#print("Code:",unparse_ast_to_code(tree))


# Define a custom NodeVisitor to traverse the AST and locate specific nodes
class CustomVisitor(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        # Dictionary to get symbolic operators
        self.op_symbols = {
            'Add': '+', 'Sub': '-', 'Mult': '*', 'Div': '/',
            'Mod': '%', 'Pow': '**', 'LShift': '<<', 'RShift': '>>',
            'BitOr': '|', 'BitXor': '^', 'BitAnd': '&', 'FloorDiv': '//'
        }

    def visit_BinOp(self, node):
        op_symbol = self.op_symbols.get(type(node.op).__name__, type(node.op).__name__)
        print(f"Found BinOp {op_symbol} at line {node.lineno}, column {node.col_offset},"
              f" column_end {getattr(node, 'end_col_offset', 'N/A')}, "
              f"left: {self.get_name(node.left)}, right: {self.get_name(node.right)}")

        # Continue visiting child nodes
        self.generic_visit(node)

    def get_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Constant):
            return repr(node.value)
        elif isinstance(node, ast.Attribute):
            return self.get_name(node.value) + '.' + node.attr
        elif isinstance(node, ast.Call):
            return self.get_name(node.func)
        elif isinstance(node, ast.BinOp):
            op_symbol = self.op_symbols.get(type(node.op).__name__, type(node.op).__name__)
            return f"{self.get_name(node.left)} {op_symbol} {self.get_name(node.right)}"
        elif isinstance(node, ast.BoolOp):
            return f" {' '.join([type(node.op).__name__ for _ in node.values])} ".join(
                [self.get_name(v) for v in node.values])
        else:
            return str(node)  # Fallback for more complex node representations


class ReplaceBinOpTransformer(ast.NodeTransformer):
    def visit_BinOp(self, node):
        # Example: replace `+` with `*` if it's an addition
        if isinstance(node.op, ast.Add):
            node.op = ast.Mult()  # Replace '+' with '*'
            print(f"Replaced '+' with '*' at line {node.lineno}, column {node.col_offset}")

        # Continue processing
        self.generic_visit(node)
        return node


# Apply the transformer
# transformer = ReplaceBinOpTransformer()
# modified_tree = transformer.visit(tree)
# print("Code:",unparse_ast_to_code(tree))
# Instantiate the visitor and visit the parsed tree
# visitor = CustomVisitor()
# visitor.visit(tree)
#print (masked_versions.get("masked_binops",[]))


# def apply_masks_to_ast(trees, masked_locations):
#     class MaskingTransformer(ast.NodeTransformer):
#         def __init__(self, masked_locationss):
#             super().__init__()
#             self.masked_locations = masked_locationss
#
#         def visit_BinOp(self, node):
#             # Check that self.masked_locations contains dictionaries with expected keys
#             for location in self.masked_locations.get("masked_binops",[]):
#                 # Matching logic
#                 if node.lineno == location["lineno"] and node.col_offset == location["col_offset"]and node.end_col_offset == location["end_col_offset"]:
#                     # Replace the operator with <mask> by inserting a Name node
#                     print(f"Replacing BinOp at line {node.lineno} with <mask>")
#                     node.op = ast.Add()  # Temporary replacement with `+`
#                     node.unique_op_marker = "__MASK_OP__"  # Custom attribute for later identification
#             return self.generic_visit(node)
#
#     transformer = MaskingTransformer(masked_locations)
#     return transformer.visit(trees)
#
# masked_tree = apply_masks_to_ast(tree, masked_versions)
#
# transformed_code = unparse_ast_to_code(masked_tree)
#
# # Targeted replacement using unique placeholder
# masked_code = transformed_code.replace(" + ", " <mask> ")
# print(masked_code)

def generate_masked_versions(code):
    # Parse the code into an AST
    tree = ast.parse(code)

    # Collect all BinOp locations for operators
    operator_nodes = []

    class OperatorCollector(ast.NodeVisitor):
        def visit_BinOp(self, node):
            # Append the BinOp node and its location details
            operator_nodes.append(node)
            self.generic_visit(node)

    # Collect all operator nodes in the AST
    collector = OperatorCollector()
    collector.visit(tree)

    # Generate a version with each operator masked
    masked_versions = []

    for idx, op_node in enumerate(operator_nodes):
        # Deepcopy the tree to avoid modifying the original AST
        modified_tree = copy.deepcopy(tree)

        # Access the operator in the modified tree and replace it with <mask>
        current_op_node = modified_tree.body[0]  # Assuming a single function or statement for simplicity

        # Navigate to the correct operator node
        for _ in range(idx):
            current_op_node = next(ast.iter_child_nodes(current_op_node))

        # Replace operator with <mask> for this specific version
        if isinstance(current_op_node, ast.BinOp):
            current_op_node.op = ast.Name(id='<mask>', ctx=ast.Load())

        # Unparse the modified tree to source code and add to versions list
        masked_code = unparse_ast_to_code(modified_tree)
        masked_versions.append(masked_code)

    return masked_versions


def replace_line_in_code(original_code, lineno, new_line):
    lines = original_code.splitlines()
    # Get the indentation of the original line
    original_indent = re.match(r"(\s*)", lines[lineno - 1]).group(1)
    # Prepend the indentation to the new line
    lines[lineno - 1] = f"{original_indent}{new_line}"
    return "\n".join(lines)

print(replace_line_in_code(code, 7, "self.width * self.height = self.height"))

# # Sample code
# code = "return self.width * self.height + self.height"
# masked_versions = generate_masked_versions(code)
#
# # Display each masked version
# for version in masked_versions:
#     print(version)
#
# def mask_code_from_json(code, masked_versions):
#     tree = parse_code_to_ast(code)
#
#     masked_locations = masked_versions["masked_binops"]
#
#     masked_tree = apply_masks_to_ast(tree, masked_locations)
#
#     return unparse_ast_to_code(masked_tree)


