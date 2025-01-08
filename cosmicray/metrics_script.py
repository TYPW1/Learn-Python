import json


def load_mutation_results(file_path):
    """Load mutation results from a JSON file with nested structure."""
    with open(file_path, 'r') as file:
        # Read and parse the file as a list of JSON objects
        data = json.load(file)

        # Flatten the data structure
        flattened_results = []
        for entry in data:
            if isinstance(entry, list):  # Handle nested lists
                flattened_results.extend(entry)
            else:
                flattened_results.append(entry)

        return flattened_results


def calculate_mutation_metrics(results):
    """Calculate metrics based on mutation testing results."""
    total_mutants = len(results)
    killed_mutants = sum(1 for result in results if result.get("test_outcome") == "killed")
    survived_mutants = sum(1 for result in results if result.get("test_outcome") == "survived")
    timed_out = sum(1 for result in results if result.get("test_outcome") == "timeout")
    errors = sum(1 for result in results if result.get("worker_outcome") == "error")

    # Calculate mutation score
    mutation_score = (killed_mutants / total_mutants) * 100 if total_mutants > 0 else 0

    return {
        "total_mutants": total_mutants,
        "killed_mutants": killed_mutants,
        "survived_mutants": survived_mutants,
        "timed_out": timed_out,
        "errors": errors,
        "mutation_score": mutation_score
    }


def main():
    # Path to the mutation results JSON file
    file_path = "mutation_results.json"  # Update with the correct path

    # Load the mutation results
    mutation_results = load_mutation_results(file_path)

    # Calculate metrics
    metrics = calculate_mutation_metrics(mutation_results)

    # Print the metrics
    print(json.dumps(metrics, indent=4))


if __name__ == "__main__":
    main()
