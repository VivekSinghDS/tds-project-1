import subprocess
import os 
def run_a2(input_path: str, package: str, version: str):
    try:
        if os.environ.get('AUTH'):
            input_path = "." + input_path if input_path[0] != '.' else input_path

        def is_allowed_path(file_path: str) -> bool:
            abs_path = os.path.abspath(file_path)
            return abs_path.startswith("/data/")
        
        if not is_allowed_path(input_path):
            raise PermissionError(f"Access outside /data/ is not allowed: {input_path}")

        
        subprocess.run(["npm", "install", "-g", f"{package}@{version}"], check=True)

        # Run prettier to format the file in-place
        subprocess.run([f"{package}", "--write", input_path], check=True)

        print(f"Formatted {input_path} successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")


# from datetime import datetime
# import re
# date_formats = [
#     r'([A-Za-z]{3} \d{1,2}, \d{4})',   # Jan 01, 2024
#     r'(\d{1,2}-[A-Za-z]{3}-\d{4})',   # 01-Jan-2024
#     r'(\d{4}-\d{2}-\d{2})',           # 2024-01-01
#     r'(\d{4}/\d{2}/\d{2})',           # 2024/01/01
#     r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})'  # 2024/01/01 12:00:00
# ]

# # Function to parse a date from a string
# def parse_date(date_str):
#     for fmt in ['%b %d, %Y', '%d-%b-%Y', '%Y-%m-%d', '%Y/%m/%d', '%Y/%m/%d %H:%M:%S']:
#         try:
#             return datetime.strptime(date_str, fmt)
#         except ValueError:
#             continue
#     return None

# # Read file
# with open('./data/dates.txt', 'r') as f:
#     lines = f.readlines()

# wednesday_count = 0

# for line in lines:
#     line = line.strip()
#     if not line:
#         continue

#     # Extract potential date using regex
#     for pattern in date_formats:
#         match = re.search(pattern, line)
#         if match:
#             date_str = match.group(1)
#             date_obj = parse_date(date_str)
#             if date_obj and date_obj.weekday() == 2:  # Wednesday
#                 wednesday_count += 1
#             break  # Stop after the first match to avoid double counting


# # print(f'Number of Wednesdays: {wednesday_count}')
