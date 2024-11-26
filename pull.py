import requests
import json
import os
from pathlib import Path
import sys

from download import *

# Your Canvas API token
API_TOKEN = sys.argv[-1]

# The Canvas base URL (your school's Canvas instance domain)
BASE_URL = sys.argv[-2]

TOMATO_PATH = sys.argv[-3]

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
            return f"pset{number}", True
    return name, False

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
        directory_name, is_pset = standardize_assignment_name(safe_assignment_name)
        directory_path = os.path.join(base_directory, directory_name)

        # Check if the directory already exists
        if not Path(directory_path).exists():
            # prompt the user whether they want to create the directory
            # if they don't, skip this assignment
            user_input = input(f"Confirm pull '{assignment_name}'? (y/n): ").strip().lower()
            if user_input != 'y':
                print(f"Aborted pulling '{assignment_name}'.")
                continue

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

            
            # often, there's an accompanying pdf file that needs to be downloaded
            # the name of the file will be in the assignment description
            # for instance ps4.pdf</a>
            # extract the name of the file by looking for ".pdf</a>"
            pdf_name = ''
            # print(assignment['description'])
            for i in range(len(assignment['description'])):
                if assignment['description'][i:i+5] == '.pdf<':
                    # go backwards until you find the start of the file name, which starts after ">"
                    j = i
                    while assignment['description'][j] != '>':
                        j -= 1
                    pdf_name = assignment['description'][j+1:i+4]
                    break
            if pdf_name:
                # download the pdf file
                print(f"Downloading attachment '{pdf_name}' for assignment '{assignment_name}'...")
                actual_file_id = find_actual_file_id(COURSE_ID, pdf_name)
                if is_pset:
                    pset_number = assignment_name[4:]
                    downloaded_name = f"problemset{pset_number}.pdf"
                else:
                    downloaded_name = pdf_name
                download_file(actual_file_id, directory_path, downloaded_name)

            if is_pset:
                # create an instance of pset latex template
                with open(TOMATO_PATH+'/pset_template.tex', 'r') as f:
                    template = f.read()
                with open(f'{directory_path}/{directory_name}.tex', 'w') as f:
                    f.write(template)

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