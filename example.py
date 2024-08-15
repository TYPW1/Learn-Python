import tokenize
from io import BytesIO
import ast

code= """
class test():
    def greet(name):
        return(f"Hello {name}!")

print(greet("World"))
"""

"""tokens = tokenize.tokenize(BytesIO(code.encode("utf-8")).readline)
for token in tokens:
    print(token)"""

""""
parsed_code = ast.parse(code)
"""



class FunctionNameExtractor (ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        print(f"Found function: {node.name}")
        self.generic_visit(node)

parsed_code = ast.parse(code)

extractor = FunctionNameExtractor()
extractor.visit(parsed_code)

print(ast.dump(parsed_code, indent = 4))