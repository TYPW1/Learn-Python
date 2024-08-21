import ast

code = """
class pete:
    def greet(name):
        print(f'Hello, {name}!')
"""


class FunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = []

    def visit_ClassDef(self, nodes):
        # print(f"Function name: {node.name}")
        # print(ast.dump(node, indent=4, include_attributes=True))
        self.functions.append(nodes)
        # self.generic_visit(node)


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
