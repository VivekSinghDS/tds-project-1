def run_a6(docs_directory: str, output_path: str):
    import os
    import glob
    import json
    if os.environ.get('AUTH'):
        docs_directory = "." + docs_directory if docs_directory[0] != '.' else docs_directory
        output_path = "." + output_path if output_path[0] != '.' else output_path
        
    def is_allowed_path(file_path: str) -> bool:
        abs_path = os.path.abspath(file_path)
        return abs_path.startswith("/data/")
            
    if not is_allowed_path(docs_directory) or not is_allowed_path(output_path):
        raise PermissionError(f"Access outside /data/ is not allowed: {docs_directory} or {output_path}")
    index = {}

    # Find all Markdown files
    md_files = glob.glob(os.path.join(docs_directory, "**/*.md"), recursive=True)

    for md_file in md_files:
        with open(md_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("# "):  # First H1 occurrence
                    title = line[2:].strip()
                    filename = os.path.relpath(md_file, docs_directory)
                    index[filename] = title
                    break  # Stop after the first H1

    # Write the index to JSON
    with open(os.path.join(output_path), "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    print("Index created successfully!")
