import os
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import numpy as np

def validate_code(code):
    """
    Validates the generated code by checking if it satisfies the prompt.
    Specifically, it checks if the function `add_numbers` works correctly.
    """
    try:
        # Dynamically execute the code
        exec(code, globals())
        # Test cases to validate the function
        result1 = add_numbers(2, 3)  # Should return 5
        result2 = add_numbers([1, 2], [3, 4])  # Should return [4, 6]
        # Check results
        if result1 == 5 and np.array_equal(result2, [4, 6]):
            return True
    except Exception as e:
        print(f"Validation failed: {e}")
    return False

def main():
    # Specify the model
    MODEL_NAME = "Salesforce/codet5p-220m"
    OUTPUT_DIR = "generated_humaneval"

    # Load the HumanEval dataset
    print("Loading HumanEval dataset...")
    dataset = load_dataset("openai/openai_humaneval", split="test")

    # Load tokenizer and model
    print("Loading CodeT5+ model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

    # Define the prompt
    prompt = """
    Write a Python function `add_numbers(a, b)` that takes two numbers or two arrays and returns their element-wise sum.
    Use NumPy for array operations. If the inputs are not arrays, treat them as scalars. Include a docstring for the function.
    """
    inputs = tokenizer(prompt, return_tensors="pt")

    # Generate multiple outputs
    print("Generating multiple code samples...")
    outputs = model.generate(
        inputs.input_ids,
        max_length=150,
        do_sample=True,
        temperature=0.7,
        num_return_sequences=3  # Generate 3 variations
    )

    # Validate each generated code
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for idx, output in enumerate(outputs):
        generated_code = tokenizer.decode(output, skip_special_tokens=True)
        print(f"\nGenerated Code {idx + 1}:\n{generated_code}")

        if validate_code(generated_code):
            print(f"Valid code found! Saving to {OUTPUT_DIR}/valid_output.py")
            output_file = os.path.join(OUTPUT_DIR, "valid_output.py")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(generated_code)
            return

    print("No valid code found.")

if __name__ == "__main__":
    main()
