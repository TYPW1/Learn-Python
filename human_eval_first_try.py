# import openai
# from openai import OpenAI
# from dotenv import load_dotenv
# import os
#
# load_dotenv()
#
# openai_api_key = os.getenv("OPENAI_API_KEY")
#
# problem_prompt = """
# write a  Python function named 'is_palindrome' that checks whether a string is  a palindrome
# """
#
# client = openai.OpenAI(api_key=openai_api_key)
#
# response = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": problem_prompt,
#         }
#     ],
#     model="gpt-3.5-turbo",  # Use GPT-4 if you have access
# )
#
# # Output the generated code
# #print(response.choices[0].message.content.strip())
#
#
# def is_palindrome(s: str) -> bool:
#     return s == s[::-1]
#
#
# test_cases = [
#     ("racecar", True),
#     ("hello", False),
#     ("madam", True),
#     ("python", False)
# ]
# for s, expected in test_cases:
#     result = is_palindrome(s)
#     print(f"Input: {s}, Output: {result}, Expected: {expected}, Test Passed: {result == expected}")


import datasets
import os
import openai
import re
import ast

from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

# load datasets from hugging interface
human_eval = datasets.load_dataset("openai_humaneval")

problem = human_eval['test'][163]['prompt']
#print(problem)

# Load GPT-Neo for code generation (you can also use GPT-3-based models from OpenAI)
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")

client = openai.OpenAI(api_key=openai_api_key)


def generate_function_logic(prompt):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o"
    )
    return response.choices[0].message.content.strip()


def extract_function_code(generated_output):
    """
    Extracts the function code from the generated output.
    It uses a regex pattern to capture the function definition and body,
    and removes comments and docstrings.
    """
    # Step 1: Extract the function using regex (detect def and extract the block until it ends)
    function_code_match = re.search(r"```python(.*?)```", generated_output, re.DOTALL)

    if function_code_match:
        func_code = function_code_match.group(1).strip()
    else:
        raise ValueError("No function code found in the generated output.")

    # Step 2: Parse the code using AST to remove docstrings and comments
    tree = ast.parse(func_code)

    # Remove docstrings by replacing them with empty strings
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if ast.get_docstring(node):
                node.body = [n for n in node.body if not isinstance(n, ast.Expr) or not isinstance(n.value, ast.Str)]

    # Remove comments by filtering out comments from the source code
    clean_code = ast.unparse(tree)  # Python 3.9+

    return clean_code


def test_generated_function(problem, generated_function_code):
    """
    This function dynamically defines the generated function using `exec()`
    and runs the HumanEval test cases on it.
    """
    # Dynamically define the generated function
    exec(generated_function_code, globals())

    # Extract the test cases from the problem
    test_cases = problem['test']

    # Execute each test case and check if it passes or fails
    for test_case in test_cases:
        try:
            exec(test_case)
            print(f"Test Passed: {test_case}")
        except AssertionError:
            print(f"Test Failed: {test_case}")

# Function to automate the entire process for a HumanEval problem
def process_humaneval_problem(problem):
    # Step 1: Extract the function prompt from HumanEval dataset
    function_prompt = problem['prompt']

    # Step 2: Generate function logic using GPT-4
    generated_function_code = generate_function_logic(function_prompt)
    print("Generated Function:\n", generated_function_code)

    # Step 3: Extract the function code (removing comments/docstrings if needed)
    clean_function_code = extract_function_code(generated_function_code)
    print("Clean Function Code:\n", clean_function_code)

    # Step 4: Test the generated function against the provided test cases
    test_generated_function(problem, clean_function_code)

# Example: Process the first HumanEval problem
problem = human_eval['test'][0]  # Select the problem (0 is the index for the first problem)
process_humaneval_problem(problem)


function_code = human_eval['test'][0]['prompt']  #Get prompt from dataset
generate_function_code = generate_function_logic(function_code)
#print("Generated Function: \n", generate_function_code)

or_code =extract_function_code(generate_function_code)
#print(or_code)
