import ast

code = """
class Menu:
    def __init__(self):
        self.menu = [
            MenuItem(name="latte", water=200, milk=150, coffee=24, cost=2.5),
            MenuItem(name="espresso", water=50, milk=0, coffee=18, cost=1.5),
            MenuItem(name="cappuccino", water=250, milk=50, coffee=24, cost=3),
        ]

def outside_function():
    print("me")
"""


class Visitor(ast.NodeVisitor):
    def __init__(self):
        self.classes = []
        self.functions = []

    def visit_ClassDef(self, node):
        self.classes.append(node)
        self.generic_visit(node)
        pass

    def visit_FunctionDef(self, node):
        function_info = {
            "function_name": node.name,
            "start_lineno": node.lineno,
            "end_lineno": node.end_lineno,
        }
        self.functions.append(function_info)
        self.generic_visit(node)


def parse(codes):
    return ast.parse(codes)


def extract_nodes(tree):
    visitor = Visitor()
    visitor.visit(tree)
    print("Nodes visited by the visitor:")
    for node in visitor.functions:
        print(node)
    return visitor


tree = ast.parse(code)
extract_nodes(tree)


def is_global_function(function_node):
    for node in ast.walk(function_node):
        if isinstance(node, ast.ClassDef):
            return False  # It's inside a class, so not global
    return True


def parsing(codes):
    all_nodes = []

    tree = parse(codes)
    visitor = extract_nodes(tree)

    # It's not inside any class, so it's global

    # Collect all global functions (functions not inside classes)
    global_functions = []
    for func in visitor.functions:
        if is_global_function(func):
            all_nodes.append(func)
    """for functions in visitor.functions:f
        if isinstance(functions, ast.FunctionDef):
            function_visitor = Visitor()
            function_visitor.visit(functions)
            function_info = {
                "functions": function_visitor.functions,
            }
        all_nodes.append(function_info)"""

    for classes in visitor.classes:
        if isinstance(classes, ast.ClassDef):
            function_visitor = Visitor()
            function_visitor.visit(classes)
            classes_info = {
                "class_name": classes.name,
                "start_line": classes.lineno,
                "end_line": classes.end_lineno,
                "functions": function_visitor.functions,
            }
        all_nodes.append(classes_info)

    return all_nodes


print(parsing(code))
