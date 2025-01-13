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

def analyze_code(prompt, test_code):
    """
    Generates code for the given prompt using GPT-4, including test cases in the prompt.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Python developer. Solve the task but include common mistakes or inefficient approaches."},
                {"role": "user", "content": f"{prompt}\nHere are the test cases the function must pass:\n{test_code}"}
            ],
            temperature=1.0
        )
        content = response.choices[0].message.content
        code_lines = []
        inside_code_block = False
        for line in content.splitlines():
            if line.strip().startswith("```"):
                inside_code_block = not inside_code_block
            elif inside_code_block:
                code_lines.append(line)
        return "\n".join(code_lines) if code_lines else content
    except Exception as e:
        return str(e)

def validate_code(generated_code, test_code):
    """
    Validates the generated code against the provided test cases.
    """
    try:
        # Ensure the generated code is syntactically valid
        ast.parse(generated_code)

        # Execute the generated code and test cases
        exec(generated_code, globals())
        exec(test_code, globals())
        return True  # Code passed the test suite
    except SyntaxError as e:
        print(f"Syntax error in code: {e}")
        return False  # Invalid syntax
    except Exception as e:
        print(f"Validation failed: {e}")
        return False  # Code failed the test suite


def inject_faults(code):
    """
    Introduces random faults into the generated code.
    """
    faults = [
        lambda x: re.sub(r"\+", "-", x),  # Replace '+' with '-'
        lambda x: re.sub(r"==", "!=", x),  # Replace '==' with '!='
        lambda x: re.sub(r"return\b", "# return", x),  # Comment out return statements
        lambda x: re.sub(r"range\((.*?)\)", r"range(\1 + 1)", x),  # Off-by-one error
        lambda x: re.sub(r"abs\((.*?)\)", r"\1", x),  # Remove abs()
        lambda x: re.sub(r":\n", ":\n    pass\n", x, 1),  # Add unnecessary `pass` statements
    ]

    # Apply a random fault
    faulty_code = random.choice(faults)(code)

    # Ensure the modified code is syntactically valid
    try:
        ast.parse(faulty_code)
        return faulty_code
    except SyntaxError:
        print("Fault injection created invalid syntax, skipping.")
        return code  # Return the original code if fault injection fails


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
        task_id = sample["task_id"]
        if task_id != "HumanEval/152":  # Replace with your desired task ID
            continue
        prompt = sample["prompt"]
        test_code = sample["test"]

        print(f"Processing task {idx + 1}/{len(dataset)}: {task_id}")

        # Generate multiple variations, but stop after saving one faulty version
        for i in range(10):  # Generate up to 10 variations
            generated_code = analyze_code(prompt, test_code)
            print(f"\nGenerated Code {i + 1} for {task_id}:\n{generated_code}")

            # Inject additional faults into the generated code
            faulty_code = inject_faults(generated_code)

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
