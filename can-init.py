import json
import os

# Prompt the user for a course ID
course_id = input("Please enter the course ID: ")

# Create a dictionary to store the course ID
data = {
    "course_id": course_id
}

# Define the filename for the JSON file
filename = "can_info.json"

# Get the current working directory
current_directory = os.getcwd()

# we want to store the info in a directory called ./tomatoes
# create the directory if it doesn't exist
tomatoes_directory = os.path.join(current_directory, ".tomatoes")
print(tomatoes_directory)
os.makedirs(tomatoes_directory, exist_ok=True)

# Create the full path for the JSON file
file_path = os.path.join(tomatoes_directory, filename)

# Write the data to the JSON file
with open(file_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f"Course ID has been saved in {file_path}")
