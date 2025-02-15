def run_a3(input_path: str, output_path: str, weekday: str):
    from datetime import datetime
    import os 
    if os.environ.get('AUTH'):
        input_path = "." + input_path if input_path[0] != '.' else input_path
        output_path = "." + output_path if output_path[0] != '.' else output_path

    def is_allowed_path(file_path: str) -> bool:
        abs_path = os.path.abspath(file_path)
        return abs_path.startswith("/data/")
    
    if not is_allowed_path(input_path) or not is_allowed_path(output_path):
        raise PermissionError(f"Access outside /data/ is not allowed: {input_path} or {output_path}")


    date_formats = [
        "%d-%b-%Y", "%b %d, %Y", "%Y-%m-%d", "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S", "%d-%m-%Y", "%m %d, %Y"
    ]
    days = {
        "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
    }
    wednesday_count = 0

    # Read and process dates
    with open(input_path, "r") as file:
        for line in file:
            date_str = line.strip()
            if not date_str:
                continue  # Skip empty lines

            parsed_date = None
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(date_str, fmt)
                    break  # Stop if parsing is successful
                except ValueError:
                    pass  # Try next format

            if parsed_date and parsed_date.weekday() == days[weekday.lower()]:  # Wednesday = 2
                wednesday_count += 1

    # Write result to output file
    with open(output_path, "w") as file:
        file.write(str(wednesday_count))

    print(f"Number of Wednesdays: {wednesday_count}")
