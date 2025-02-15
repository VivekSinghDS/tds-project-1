def run_a4(input_path, output_path, keys):
    import json
    import os
    import ast
    keys = ast.literal_eval(keys)
    if os.environ.get('AUTH'):
        input_path = "." + input_path if input_path[0] != '.' else input_path

        output_path = "." + output_path if output_path[0] != '.' else output_path

    def is_allowed_path(file_path: str) -> bool:
        abs_path = os.path.abspath(file_path)
        return abs_path.startswith("/data/")
            
    if not is_allowed_path(input_path) or not is_allowed_path(output_path):
        raise PermissionError(f"Access outside /data/ is not allowed: {input_path} or {output_path}")

    # Read the JSON data
    with open(input_path, "r") as f:
        contacts = json.load(f)
    print(keys)
    # Sort contacts by last_name, then first_name
    sorted_contacts = sorted(contacts, key=lambda c: tuple(c[key] for key in keys))
    # Write sorted data to output file
    with open(output_path, "w") as f:
        json.dump(sorted_contacts, f, indent=2)

    print("Sorting complete. Sorted contacts saved to", output_path)
