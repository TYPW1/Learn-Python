import json
import humaneval_integration  # This is the new module for HumanEval integration
import os
import pytest


from cb.replacement_mutants import ReplacementMutant
from os.path import join
from pathlib import Path
from util import get_file_names_from_user, load_file
from masking_module import generate_masked_code_versions
from predictions import make_predictions_and_generate_mutants
from file_parser import parse_python_file, extract_all_definitions, parse_selected_files, tree_to_source
from shutil import copyfile
from contract_corpus_integration import process_contract_corpus
from cb.json_locs_parser import ListFileLocations
from cb.__init__ import  predict_json_locs, predict_locs
from cb.code_bert_mlm import CodeBertMlmFillMask
from cb.job_config import JobConfig, NOCOSINE_JOB_CONFIG

DEFAULT_BASE_DIR = join(Path(__file__).parent.parent, 'tests', 'res', 'samples')
DEFAULT_OUTPUT_DIR = join(Path(__file__).parent.parent, 'output')


def process_humaneval_dataset():
    # Step 1: Load the HumanEval dataset
    human_eval = humaneval_integration.load_humaneval_dataset()

    # Step 2: Loop through each problem in HumanEval
    for idx, problem in enumerate(human_eval['test']):
        print(f"\nProcessing HumanEval Problem {idx + 1}")

        # Step 3: Process the HumanEval problem (extract, mask, and display the results)
        masked_code, test_cases = humaneval_integration.process_humaneval_problem(problem)

        # For now, just display the masked code and test cases
        print(f"Masked Code for Problem {idx + 1}:\n{masked_code}")
        print(f"Test Cases:\n{test_cases}")


def process_contract_corpus_files():
    code_to_tests = process_contract_corpus()  # Call to process the contract corpus
    for code_file, tests in code_to_tests.items():
        print(f"Processed {code_file} with tests: {tests}")

# def extract_masked_code_with_predictions(file_locs, cbm, max_size=512):
#     masked_code_data = []
#     mask_token = cbm.tokenizer.mask_token  # Automatically fetch the correct mask token
#
#     for file_loc in file_locs.__root__:
#         print(f"Processing file: {file_loc.file_path}")
#         for class_loc in file_loc.classPredictions:
#             print(f"  Class: {class_loc.qualifiedName}")
#             for method_loc in class_loc.methodPredictions:
#                 print(f"    Method: {method_loc.methodSignature}")
#                 method_start = method_loc.codePosition.startPosition
#                 method_end = method_loc.codePosition.endPosition
#                 method_string = load_file(file_loc.file_path)[method_start: method_end + 1]
#
#                 for line_loc in method_loc.line_predictions:
#                     for location in line_loc.locations:
#                         code_position = location.codePosition
#                         start = code_position.startPosition
#                         end = code_position.endPosition
#
#                         # Create masked code
#                         masked_method_string = (
#                             load_file(file_loc.file_path)[method_start: start]
#                             + mask_token
#                             + load_file(file_loc.file_path)[end + 1: method_end + 1]
#                         )
#                         print(f"Masked string: {masked_method_string}")
#
#                         try:
#                             # Call the CodeBert model
#                             predictions = cbm.call_func(masked_method_string)
#                             print(f"Raw predictions: {predictions}")
#
#                             # Extract token strings from ListCodeBertPrediction
#                             if isinstance(predictions, list):
#                                 prediction_tokens = []
#                                 for pred in predictions:
#                                     if hasattr(pred, "__root__") and isinstance(pred.__root__, list):
#                                         for codebert_pred in pred.__root__:
#                                             prediction_tokens.append(codebert_pred.token_str)
#                                     else:
#                                         raise ValueError(f"Unexpected prediction format: {pred}")
#                             else:
#                                 raise ValueError("Predictions are not a list of ListCodeBertPrediction objects")
#
#                             # Append data
#                             masked_code_data.append({
#                                 "file": file_loc.file_path,
#                                 "class": class_loc.qualifiedName,
#                                 "method": method_loc.methodSignature,
#                                 "line": line_loc.line_number,
#                                 "masked_code": masked_method_string,
#                                 "predictions": prediction_tokens,
#                             })
#                             print(f"Appended data for {masked_method_string}: {prediction_tokens}")
#                         except Exception as e:
#                             print(f"Error generating predictions for {masked_method_string}: {e}")
#
#     print(f"Masked code data generated: {masked_code_data}")
#     return masked_code_data


def generate_mutants(file_locs, cbm, output_dir, job_config, max_size=512, batch_size=16):
    """
    Generates mutants for each file location and stores them in the output directory.

    :param file_locs: Parsed `ListFileLocations` object.
    :param cbm: CodeBertMlmFillMask model for masking and prediction.
    :param output_dir: Directory where mutants will be saved.
    :param job_config: JobConfig object for prediction configuration.
    :param max_size: Maximum token size for the model input.
    :param batch_size: Batch size for predictions.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Global mutant ID counter
    global_mutant_id = 0

    for file_loc in file_locs.__root__:
        file_path = file_loc.file_path
        file_string = load_file(file_path)

        for class_loc in file_loc.classPredictions:
            for method_loc in class_loc.methodPredictions:
                method_start = method_loc.codePosition.startPosition
                method_end = method_loc.codePosition.endPosition
                method_string = file_string[method_start:method_end + 1]

                for line_loc in method_loc.line_predictions:
                    for location in line_loc.locations:
                        # Prepare mutation
                        code_position = location.codePosition
                        start = code_position.startPosition
                        end = code_position.endPosition
                        original_token = file_string[start:end + 1]

                        # Create masked version
                        masked_string = (
                            file_string[method_start:start]
                            + cbm.tokenizer.mask_token
                            + file_string[end + 1:method_end + 1]
                        )

                        try:
                            # Generate predictions
                            predictions = cbm.call_func(masked_string)
                            if not predictions:
                                print(f"No predictions generated for masked string: {masked_string}")
                                continue

                            for pred in predictions:
                                if not hasattr(pred, "__root__") or not pred.__root__:
                                    print(f"No valid predictions in: {pred}")
                                    continue

                                for sub_pred in pred.__root__:
                                    # Extract prediction token string
                                    replacement = sub_pred.token_str

                                    # Create a unique mutant instance
                                    mutant = ReplacementMutant(
                                        id=global_mutant_id,  # Use global mutant ID
                                        file_path=file_path,
                                        start=start,
                                        end=end + 1,
                                        replacement=replacement
                                    )

                                    # Save mutant to a unique directory
                                    mutant_output_dir = os.path.join(output_dir, f"mutant_{global_mutant_id}")
                                    if not os.path.exists(mutant_output_dir):
                                        os.makedirs(mutant_output_dir)

                                    # Apply mutation and save the resulting file
                                    mutated_code = mutant.apply_mutation(file_string)
                                    mutated_file_path = os.path.join(mutant_output_dir, Path(file_path).name)

                                    with open(mutated_file_path, 'w', encoding='utf-8') as mutated_file:
                                        mutated_file.write(mutated_code)

                                    # Log the mutant saving process
                                    print(f"Saved mutant {global_mutant_id} to {mutated_file_path}")

                                    # Increment the global mutant ID
                                    global_mutant_id += 1
                        except Exception as e:
                            print(f"Error while generating mutants for masked string: {masked_string}\n{e}")



def process_custom_files():
    # Get file paths from the user
    file_paths = get_file_names_from_user(DEFAULT_BASE_DIR)

    if not file_paths:
        print("No files selected.")
        return

    # Parse selected files into ListFileLocations JSON format
    if not os.path.exists(DEFAULT_OUTPUT_DIR):
        os.makedirs(DEFAULT_OUTPUT_DIR)

    output_json_path = os.path.join(DEFAULT_OUTPUT_DIR, 'results.json')
    parse_selected_files(file_paths, DEFAULT_OUTPUT_DIR)  # Saves to 'results.json'

    # Load the JSON and transform it to match ListFileLocations expectations
    with open(output_json_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    # Extract the list under "fileLocations" and assign it to "__root__"
    transformed_json_data = {"__root__": json_data["fileLocations"]}

    # Validate and inspect transformed_json_data before passing to Pydantic
    for file_entry in transformed_json_data["__root__"]:
        # Adjust for 'file_path' instead of 'filePath'
        file_path = file_entry.get("file_path") or file_entry.get("filePath")
        if not file_path:
            raise ValueError(f"Missing or invalid 'filePath' in entry: {file_entry}")
        # Ensure absolute paths for consistency
        file_entry["file_path"] = str(Path(file_path).resolve())


    # Serialize the transformed JSON back to a temporary file (optional, for inspection)
    temp_output_path = os.path.join(DEFAULT_OUTPUT_DIR, 'transformed_results.json')
    with open(temp_output_path, 'w', encoding='utf-8') as temp_file:
        json.dump(transformed_json_data, temp_file, indent=4)

    # Parse the transformed JSON as ListFileLocations object
    file_locs = ListFileLocations.parse_file(temp_output_path)

    # Debugging: Check parsed file_locs
    print(f"Parsed file locations: {file_locs}")
    print("type of file locs location", type(file_locs))

    # Initialize the CodeBert model for predictions
    cbm = CodeBertMlmFillMask()

    # Use preconfigured NOCOSINE_JOB_CONFIG to disable cosine similarity
    job_config = NOCOSINE_JOB_CONFIG

    # Generate mutants and save them
    mutant_output_dir = os.path.join(DEFAULT_OUTPUT_DIR, "mutants")
    generate_mutants(file_locs, cbm, mutant_output_dir, job_config)

    # Run predictions on the masked code using the ListFileLocations object
    #predict_locs(file_locs, cbm, job_config)

    # masked_code_data = extract_masked_code_with_predictions(file_locs, cbm)
    #
    # # Optionally save to a file
    # masked_code_output_path = os.path.join(DEFAULT_OUTPUT_DIR, 'masked_code.json')
    # with open(masked_code_output_path, 'w', encoding='utf-8') as json_file:
    #     json.dump(masked_code_data, json_file, indent=4)
    # print(f"Masked code saved to {masked_code_output_path}")

    print("Processing and predictfions completed.")



if __name__ == "__main__":
    # Ask the user whether they want to process custom files or HumanEval dataset
    mode = input("Select mode: (1) Process Custom Files, (2) Process HumanEval Dataset: ")

    if mode == "1":
        process_custom_files()
        #parse_selected_files(get_file_names_from_user(DEFAULT_BASE_DIR), DEFAULT_OUTPUT_DIR)
        #generate_masked_code_versions(get_file_names_from_user(DEFAULT_BASE_DIR), DEFAULT_OUTPUT_DIR)
        #try_unparse()
    elif mode == "2":
        # Process the HumanEval dataset instead
        #process_humaneval_dataset()
        process_contract_corpus()
    else:
        print("Invalid option. Please select 1 or 2.")


