from typing import List, Tuple
import ast

def calculate_code_lines_offset(code):
  code.code_lines


def get_node_position(node, source_code):
    """
    Get the start character position of an AST node if it has one.

    Parameters:
    - node: The AST node.
    - source_code: The source code as a string.

    Returns:
    - The start character position of the node in the source code if available, otherwise None.
    """
    # Check if the node has lineno and col_offset attributes
    if hasattr(node, 'lineno') and hasattr(node, 'col_offset'):
        lines = source_code.splitlines()
        lineno = node.lineno - 1  # Line numbers in AST start at 1
        col_offset = node.col_offset
        char_position = sum(len(line) + 1 for line in lines[:lineno]) + col_offset
        return char_position
    else:
        return None  # Return None if node has no position info


def get_op_position_in_chars(if_cdt, op_txt, source_code, previous_op_end=0):
    """
    We need to sum:
    - the previous lines length
    - the condition col offset
    - the position of the operator in the condition

    """
    # original code of the condition:
    original_condition_txt = ast.get_source_segment(code, if_cdt)
    #print("_" + original_condition_txt + "_")
    if_cdt_position = get_node_position(if_cdt, code)

    condt_offset = 0
    if previous_op_end > 0:
        condt_offset = previous_op_end - if_cdt_position

    op_pos_start = get_node_position(if_cdt, code) + original_condition_txt.find(op_txt, condt_offset)
    op_pos_end = op_pos_start + len(op_txt)
    #print("searching for: "+op_txt+ " got the position of _" + code[op_pos_start:op_pos_end]+"_")
    return op_pos_start, op_pos_end



def get_op_text(op) -> str:
    if isinstance(op, ast.Gt):
        op_txt = ">"
    elif isinstance(op, ast.GtE):
        op_txt = ">="
    elif isinstance(op, ast.Eq):
        op_txt = "=="
    elif isinstance(op, ast.NotEq):
        op_txt = "!="
    elif isinstance(op, ast.Lt):
        op_txt = "<"
    elif isinstance(op, ast.LtE):
        op_txt = "<="
    return op_txt


def find_if_conditional_operators(code) -> Tuple[Tuple[int],str]:
    tree = ast.parse(code)
    operator_positions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            for if_cdt_child in ast.walk(node.test):
                if isinstance(if_cdt_child, ast.Compare):
                    # if we have two ops in the same conditions
                    # e.g. a < b < c
                    # we have to start searching for the position after the end of the first.
                    previous_op_end = 0
                    # looping through the ops of a comparison.
                    for op in if_cdt_child.ops:
                        op_txt = get_op_text(op)
                        # Load the start and end position of the operator.
                        pos = get_op_position_in_chars(if_cdt_child, op_txt, code, previous_op_end)
                        previous_op_end = pos[1]
                        # Keep the position and the inverted operator in a list.
                        operator_positions.append((pos, op_txt))

    return operator_positions


code = """
x = 10
y = 5

while x <= 0 and x < 0:
  x = x + 5
  print("x increased by 5")


if x >= y and x != 0:
  print("x is greater than y and x is not zero")
else:
  print("x is less than y or x is zero")

class MyClass:
  def __init__(self, a, b):
    self.a = a
    self.b = b

  def compare_values(self):
    if self.a > self.b:
      c = self.a < self.b
      print("a is greater than b")
    elif self.a == self.b:
      print("a is equal to b")
    else:
      print("a is less than b")


my_object = MyClass(7, 3)
my_object.compare_values()
"""

operator_positions = find_if_conditional_operators(code)
print("Operator positions:", operator_positions)