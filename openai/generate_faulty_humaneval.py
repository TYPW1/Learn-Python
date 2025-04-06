import ast
import os
import re
import random
from openai import OpenAI
from datasets import load_dataset
from dotenv import load_dotenv

# Load API key from environment variables or .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_code(prompt):
    """
    Generates faulty code for the given prompt using GPT-4.
    """
    try:
        # Generate code with intentional faults using GPT-4
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "You are a beginner python developper make beginner's mistakes that will fail any test applied to it. do not use any modules."},
                {"role": "user", "content": f"{prompt}\nPlease generate the code for the given task."}
            ],
            temperature=1.0
        )

        # Extract the generated code from the response
        content = response.choices[0].message.content

        return content  # Return the generated faulty code

    except Exception as e:
        return f"An error occurred: {str(e)}"


def extract_code(text):
    """
    Extracts the Python code between triple backticks from a string.

    Args:
        text (str): The input string containing the code.

    Returns:
        str: The extracted Python code.
    """
    # Use a regular expression to find the code block between triple backticks
    code_match = re.search(r'```python\n(.*?)```', text, re.DOTALL)

    if code_match:
        # Return the code inside the backticks
        return code_match.group(1).strip()
    else:
        return "No code block found."

def validate_code(generated_code, test_code):
    """
    Validates the generated code against the provided test cases.
    Ensures that all necessary modules are imported.
    """
    try:
        # Parse the code to check for imports and usage of external modules
        tree = ast.parse(generated_code)

        # Find all module imports in the code (both regular imports and from imports)
        imports = [node.name for node in ast.walk(tree) if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom)]

        # Check for any used modules in the code
        used_modules = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                used_modules.add(node.id)

        # Compare used modules with imported modules to find any missing imports
        missing_imports = used_modules - set(imports)

        if missing_imports:
            raise ValueError(f"These modules are used but not imported: {', '.join(missing_imports)}")

        # Ensure the generated code is syntactically valid
        exec(generated_code, globals())
        exec(test_code, globals())
        return True  # Code passed the test suite

    except SyntaxError as e:
        print(f"Syntax error in code: {e}")
        return False  # Invalid syntax
    except ValueError as ve:
        print(f"Validation failed: {ve}")
        return False  # Missing import(s)
    except Exception as e:
        print(f"Validation failed: {e}")
        return False  # Code failed the test suite


def save_faulty_version(code, task_id, version):
    """
    Saves the faulty version to the appropriate directory.
    """
    # Construct the directory path based on the task_id
    task_dir = os.path.join("faulty_versions", os.path.dirname(task_id))
    os.makedirs(task_dir, exist_ok=True)  # Ensure the directory exists

    # Construct the output file path
    output_file = os.path.join(task_dir, f"{os.path.basename(task_id)}_faulty_{version}.py")

    # Save the faulty version
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Saved faulty version to {output_file}")


def main():
    print("Loading HumanEval dataset...")
    dataset = load_dataset("openai/openai_humaneval", split="test")
    OUTPUT_DIR = "faulty_versions"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for idx, sample in enumerate(dataset):
        if idx >= 3:
            break
        task_id = sample["task_id"]
        # if task_id != "HumanEval/0":  # Replace with your desired task ID
        #     continue
        prompt = sample["prompt"]
        test_code = sample["test"]

        print(f"Processing task {idx + 1}/{len(dataset)}: {task_id}")

        # Generate multiple variations, but stop after saving one faulty version
        for i in range(10):  # Generate up to 10 variations
            generated_code = analyze_code(prompt)
            print(f"\nGenerated Code {i + 1} for {task_id}:\n{generated_code}")

            # Inject additional faults into the generated code
            faulty_code = extract_code(generated_code)

            # Validate the faulty version
            if not validate_code(faulty_code, test_code):  # Save only if it fails
                print(f"Faulty version found for {task_id}. Saving...")
                save_faulty_version(faulty_code, task_id, i + 1)
                break  # Stop after saving the first faulty version
            else:
                print(f"Generated code for {task_id} passed the test suite (not faulty).")

    print("\nProcessing complete.")


if __name__ == "__main__":
    main()
