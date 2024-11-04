import copy
from fileinput import lineno
import json
import ast
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
            "original": "*"
        },
        {
            "left": "self.width",
            "op": "<mask>",
            "right": "self.height",
            "lineno": 7,
            "col_offset": 15,
            "original": "*"
        },
        {
            "left": "2",
            "op": "<mask>",
            "right": "self.width + self.height",
            "lineno": 10,
            "col_offset": 15,
            "original": "*"
        },
        {
            "left": "self.width",
            "op": "<mask>",
            "right": "self.height",
            "lineno": 10,
            "col_offset": 20,
            "original": "+"
        },
        {
            "left": "2",
            "op": "<mask>",
            "right": "self.width + self.height",
            "lineno": 14,
            "col_offset": 11,
            "original": "*"
        },
        {
            "left": "self.width",
            "op": "<mask>",
            "right": "self.height",
            "lineno": 14,
            "col_offset": 16,
            "original": "+"
        },
        {
            "left": "7",
            "op": "<mask>",
            "right": "5",
            "lineno": 18,
            "col_offset": 9,
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

def parse_code_to_ast(code):
    return ast.parse(code)

def apply_masks_to_ast(tree, masked_locations):
    class MaskingTransformer(ast.NodeTransformer):
        def __init__(self, masked_locations):
            super().__init__()
            # Check if masked_locations is a list of dictionaries
            if not isinstance(masked_locations, list):
                raise TypeError("masked_locations should be a list of dictionaries")
            self.masked_locations = masked_locations

        def visit_BinOp(self, node):
            # Check that self.masked_locations contains dictionaries with expected keys
            for location in self.masked_locations:
                if not isinstance(location, dict):
                    raise TypeError("Each item in masked_locations should be a dictionary")
                if "lineno" not in location or "col_offset" not in location:
                    raise KeyError("Each location should contain 'lineno' and 'col_offset' keys")

                # Matching logic
                if node.lineno == location["lineno"] and node.col_offset == location["col_offset"]:
                    # Replace the operator with <mask> by inserting a Name node
                    node.op = ast.Name(id=MASK, ctx=ast.Load())
            self.generic_visit(node)
            return node

    transformer = MaskingTransformer(masked_locations)
    return transformer.visit(tree)


def reconstruct_code_from_ast(tree):
    return ast.unparse(tree)


def mask_code_from_json(code, masked_versions):
    tree = parse_code_to_ast(code)

    masked_locations = masked_versions["masked_binops"]

    masked_tree = apply_masks_to_ast(tree, masked_locations)

    return reconstruct_code_from_ast(masked_tree)


masked_code = mask_code_from_json(code, masked_versions)
print(f"modified code with masks", masked_code)

# def generate_mutants_with_masks(code, masked_versions, num_predictions=5):
#     #split code into lines for easier manipulation
#     lines = code.splitlines(keepends=True)
#     mutants = []
#
#     for mask_type, masks in masked_versions.items():
#         for mask_info in masks:
#             #step 1: Apply the mask to the original line
#             mutated_lines = copy.deepcopy(lines)
#             mutated_lines = replace_with_mask(mutated_lines,mask_info)
#             masked_code = "".join(mutated_lines)
#             print(f"Code with mask applied:\n{masked_code}\n{'-' * 40}")
#     return mutants

# Test the function by applying masks and generating mutants
#mutants = generate_mutants_with_masks(code, masked_versions)

