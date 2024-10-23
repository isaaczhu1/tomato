import requests
import json
import os
from pathlib import Path
import sys


# Your Canvas API token
API_TOKEN = sys.argv[-1]

# The Canvas base URL (your school's Canvas instance domain)
BASE_URL = sys.argv[-2]

# to get the course ID, start from the current directory and go up until you find a directory .tomatoes
# inside that directory, there should be a json file called can_info.json, which contains the course ID
cnt = 0
while not os.path.exists('.tomatoes'):
    os.chdir('..')
    cnt += 1
    if cnt > 10:
        raise Exception("You have not initialized the Canvas info. Run can init.")
with open('.tomatoes/can_info.json', 'r') as f:
    COURSE_ID = json.load(f)['course_id']

# print(f"Course ID: {COURSE_ID}")

# Directory to store assignments
BASE_DIRECTORY = "psets"

# Function to get all assignments from the course
def get_assignments(course_id):
    url = f"{BASE_URL}/courses/{course_id}/assignments"
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Return the list of assignments
    else:
        print(f"Failed to retrieve assignments. Status code: {response.status_code}, Response: {response.text}")
        return []

# standardized assignment names for psets
def standardize_assignment_name(name):
    '''
    if the assignment contains the substring 'set'
    and it also contains a number (possibly with more than one digit),
    return "psetn" where n is the number
    else return the original name
    '''
    if 'set' or 'Set' or 'SET' in name:
        number = ''
        for char in name:
            if char.isdigit():
                number += char
        if number:
            return f"pset{number}"
    return name

# Function to create a directory for each assignment
def create_assignment_directories(assignments, base_directory):
    # Create the base directory if it doesn't exist
    Path(base_directory).mkdir(parents=True, exist_ok=True)
    
    for assignment in assignments:
        # print(assignment)
        assignment_id = assignment['id']
        assignment_name = assignment['name']
        
        # Create a safe directory name (avoid illegal characters)
        safe_assignment_name = "".join([c if c.isalnum() else "_" for c in assignment_name])
        directory_name = standardize_assignment_name(safe_assignment_name)
        directory_path = os.path.join(base_directory, directory_name)

        # Check if the directory already exists
        if not Path(directory_path).exists():
            # Create the directory for this assignment
            Path(directory_path).mkdir(parents=True, exist_ok=True)
            
            # Create a file with the assignment information
            info_file_path = os.path.join(directory_path, "assignment_info.json")
            assignment_info = {
                "Course ID": COURSE_ID,
                "Assignment ID": str(assignment_id),
                "Title": assignment_name,
                "Due Date": assignment['due_at'] if assignment['due_at'] else "Not set",
                "Description": assignment['description'] if assignment['description'] else "No description",
                "Submission Types": assignment['submission_types'],
                "Points Possible": assignment['points_possible']
            }
            with open(info_file_path, 'w') as info_file:
                json.dump(assignment_info, info_file, indent=4)

            print(f"Pulled assignment '{assignment_name}' (ID: {assignment_id}) and created directory.")

            if False:
                # often, there's an accompanying pdf file that needs to be downloaded
                # it'll be in the assignment's description, as a substring like href=\"https://canvas.mit.edu/courses/28240/files/4521000?wrap=1\"
                if 'href' in assignment['description']:
                    # find the first instance of 'href' in the description
                    start = assignment['description'].find('href')
                    # find the first instance of 'https' after that
                    start = assignment['description'].find('https', start)
                    # find the first instance of '\"' after that
                    end = assignment['description'].find('\"', start)
                    # extract the url
                    url = assignment['description'][start:end]
                # remove the "?wrap=1" at the end of the url, and replace it with "/download"
                url = url.replace("?wrap=1", "/download")
                print(url)

        else:
            # print(f"Directory for assignment '{assignment_name}' already exists, skipping creation.")
            pass

# Main function to retrieve assignments and create directories
def main():
    # Step 1: Get assignments from Canvas
    assignments = get_assignments(COURSE_ID)

    if assignments:
        # Step 2: Create directories and store assignment information
        create_assignment_directories(assignments, BASE_DIRECTORY)

# Run the script
main()