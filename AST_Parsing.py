import ast

# Sample code to parse
code = """
x = 5
y = x + 2
print(y)
"""

# Parse the code to generate the AST
tree = ast.parse(code)

# Dump the AST for inspection
print(ast.dump(tree, annotate_fields=True, include_attributes=True, indent=4))
