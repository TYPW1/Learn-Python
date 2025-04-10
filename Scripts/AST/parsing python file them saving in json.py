import ast
import json
import os


class ASTNodeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ast.AST):
            fields = {field: getattr(obj, field) for field in obj._fields}
            fields['__class__'] = obj.__class__.__name__
            return fields
        elif isinstance(obj, list):
            return [self.default(item) for item in obj]
        return json.JSONEncoder.default(self, obj)


class PythonFileParser:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.project_structure = {
            'root': root_dir,
            'files': []
        }

    def parse_code(self, code):
        tree = ast.parse(code)
        return tree

    def parse_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()
        tree = ast.parse(code)
        return tree

    def parse_files(self, files_to_parse):
        for file_path in files_to_parse:
            parsed_tree = self.parse_file(file_path)
            self.project_structure['files'].append({
                'file_path': file_path,
                'ast': parsed_tree
            })

    def save_to_json(self, output_file):
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(self.project_structure, file, cls=ASTNodeEncoder, indent=4)


# Example usage
if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current script's directory

    # Get user input for file selection
    file_to_parse = input(f"Enter the path of the Python file to parse (relative to {root_dir}): ")
    file_path = os.path.join(root_dir, file_to_parse)

    if not os.path.isfile(file_path):
        print(f"The file {file_path} does not exist.")
    else:
        parser = PythonFileParser(root_dir)
        parser.parse_files([file_path])
        output_file = os.path.join(root_dir, 'parsed_project.json')  # Save JSON in the same directory
        parser.save_to_json(output_file)
        print(f"AST has been saved to {output_file}")
