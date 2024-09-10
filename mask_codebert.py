import ast
import json

# Step 1: Define the Visitor class to collect variable assignments
class VariableMasker(ast.NodeVisitor):
    def __init__(self):
        self.assignments = []

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.assignments.append({
                    'variable': target.id,  # Collect variable names
                    'line': node.lineno,
                    'col': node.col_offset
                })
        self.generic_visit(node)

# Step 2: Function to parse Python code and find variable names
def parse_python_code(file_content):
    tree = ast.parse(file_content)
    masker = VariableMasker()
    masker.visit(tree)
    return masker.assignments

# Step 3: Function to mask variable names in the code
def mask_variable_names(file_content, variable_names):
    masked_content = file_content
    for var in variable_names:
        # Replace the variable name with <mask>
        masked_content = masked_content.replace(var['variable'], '<mask>')
    return masked_content

# Step 4: Convert the original and masked AST into JSON
def ast_to_json(tree):
    return ast.dump(tree, annotate_fields=True)

# Step 5: Output the original and masked AST in the same JSON structure
def output_ast_comparison(original_ast, masked_ast):
    return json.dumps({
        "original": ast_to_json(original_ast),
        "masked": ast_to_json(masked_ast)
    }, indent=4)

# Step 6: Example usage
if __name__ == "__main__":
    # Example Python code that we want to mask variable names
    example_code = """
x = 10
y = x + 5
result = y * 2
"""

    # Step 7: Parse the original code to find variable names
    original_assignments = parse_python_code(example_code)

    # Step 8: Mask the variable names in the original code
    masked_code = mask_variable_names(example_code, original_assignments)

    # Step 9: Parse the original and masked code to get AST
    original_ast = ast.parse(example_code)
    masked_ast = ast.parse(masked_code)

    # Step 10: Output both original and masked AST in the same JSON structure
    ast_comparison_json = output_ast_comparison(original_ast, masked_ast)

    # Step 11: Print the result
    print(ast_comparison_json)

    # Optionally save the comparison JSON to a file
    with open('ast_comparison.json', 'w') as f:
        f.write(ast_comparison_json)
