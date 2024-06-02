import argparse
import subprocess
import re
import os

# Create the parser
parser = argparse.ArgumentParser(description='Update the version in pyproject.toml')

# Add the arguments
parser.add_argument('Path',
                    metavar='path',
                    type=str,
                    help='the path to the directory containing pyproject.toml')

# Parse the arguments
args = parser.parse_args()

# Get the latest tag
latest_tag = subprocess.check_output(['git', 'describe', '--tags']).decode('utf-8').strip()

# Remove 'v' from the start of the tag
latest_tag = re.sub('^v', '', latest_tag)


# Define a function to replace the version in the given file
def replace_version(file_path, new_version):
    with open(file_path, 'r') as file:
        file_data = file.read()

    # Replace the target string
    file_data = re.sub(r'version = ".*"', f'version = "{new_version}"', file_data)

    # Write the file out again
    with open(file_path, 'w') as file:
        file.write(file_data)


# Replace version in the files
try:
    print(f"Going to update version in pyproject.toml with path {args.Path} to {latest_tag}")
    replace_version(os.path.join(args.Path, 'pyproject.toml'), latest_tag)
except FileNotFoundError:
    print("File not found. Exiting.")
    os._exit(1)

print("Version updated successfully.")
