import subprocess
import re
import os

# Get the latest tag
latest_tag = subprocess.check_output(['git', 'describe', '--tags']).decode('utf-8').strip()

print(latest_tag)

# Remove 'v' from the start of the tag
latest_tag = re.sub('^v', '', latest_tag)

print(latest_tag)


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
    print("Going to update version in pyproject.toml")
    replace_version('pyproject.toml', latest_tag)
except FileNotFoundError:
    print("File not found. Exiting.")
    os._exit(1)

print("Version updated successfully.")
print(open("pyproject.toml").read())