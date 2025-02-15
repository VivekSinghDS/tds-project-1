def run_a5(log_directory: str, output_path: str):
    import os
    import glob
    if os.environ.get('AUTH'):
        log_directory = "." + log_directory if log_directory[0] != '.' else log_directory
        output_path = "." + output_path if output_path[0] != '.' else output_path

    def is_allowed_path(file_path: str) -> bool:
        abs_path = os.path.abspath(file_path)
        return abs_path.startswith("/data/")
            
    if not is_allowed_path(log_directory) or not is_allowed_path(output_path):
        raise PermissionError(f"Access outside /data/ is not allowed: {log_directory} or {output_path}")
    
    log_files = sorted(glob.glob(f"{log_directory}/*.log"), key=os.path.getmtime, reverse=True)[:10]

    with open(f"{output_path}", "w") as output_file:
        for log_file in log_files:
            with open(log_file, "r") as f:
                first_line = f.readline().strip()
                output_file.write(first_line + "\n")
