import os
from os.path import join
from pathlib import Path

from mbertc.load_locs import get_tokens, get_lines_offsets, token_real_pos
from mbertc.load_locs import parse_tokens_to_cbnt_obj

DEFAULT_BASE_DIR = join(Path(__file__).parent)

def get_file_names_from_user(base_dir):
    return [join(base_dir, 'example.py')]

file_paths = get_file_names_from_user(DEFAULT_BASE_DIR)


for file_path in file_paths:
    if not os.path.isfile(file_path) or not file_path.endswith(".py"):
        continue

    # Get line offsets to be used for token real position calculation
    line_offsets = get_lines_offsets(file_path)
    print(f"[DEBUG] Line offsets for {file_path}: {line_offsets}")

    # Define the line range for token extraction (adjust as needed)
    line_start = 7  # Example starting line
    line_end = 7   # Example ending line

    # Get tokens within the specified line range
    tokens = get_tokens(file_path, line_start, line_end)
    print(f"[DEBUG] Extracted tokens: {[t.token_value for t in tokens]}")

    # Calculate token real positions using line offsets
    locs = [(t, token_real_pos(t, line_offsets[t.line - 1])) for t in tokens]
    for token, pos in locs:
        print(f"[DEBUG] Token '{token.token_value}' at real position {pos}")

        # Parse tokens into structured object
        cbnt_obj = parse_tokens_to_cbnt_obj(locs, file_path=file_path, line_start=line_start, line_end=line_end)

        # Convert to JSON or output the parsed object
        cbnt_json = cbnt_obj.json()
        print(f"[DEBUG] Parsed JSON: {cbnt_json}")
        print(type(cbnt_obj))