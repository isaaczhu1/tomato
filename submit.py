import requests
import json
import os
import sys

# Your Canvas API token
API_TOKEN = sys.argv[-1]
# The Canvas base URL (your school's Canvas instance domain)
BASE_URL = sys.argv[-2]


# go up until you find the .tomatoes directory in the root
cnt = 0
while not os.path.exists('.tomatoes'):
    os.chdir('..')
    cnt += 1
    if cnt > 10:
        raise Exception("You have not initialized the Canvas info. Run tomato init")
with open('.tomatoes/can_info.json', 'r') as f:
    COURSE_ID = json.load(f)['course_id']

# get the assignment id from the name
assignment_name = sys.argv[1]
with open(f'psets/{assignment_name}/assignment_info.json', 'r') as f:
    ASSIGNMENT_ID = json.load(f)['Assignment ID']

# Path to the PDF file you want to upload
PDF_FILE_PATH = f'psets/{assignment_name}/{assignment_name}.pdf'

# Step 1: Start the file upload process by getting the upload URL
def start_file_upload(course_id, file_path):
    file_name = os.path.basename(file_path)
    
    url = f"{BASE_URL}/courses/{course_id}/assignments/{ASSIGNMENT_ID}/submissions/self/files"
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    # Payload for the initial file upload request
    payload = {
        "name": file_name,
        "size": os.path.getsize(file_path),
        "content_type": "application/pdf",  # Since you're uploading a PDF
        "parent_folder_path": "/uploads"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        return response.json()["upload_url"], response.json()["file_param"]
    else:
        print(f"Failed to start file upload. Status code: {response.status_code}, Response: {response.text}")
        return None, None

# Step 2: Upload the file to the provided URL
def upload_file(upload_url, file_param, file_path):
    with open(file_path, 'rb') as f:
        files = {
            file_param: (os.path.basename(file_path), f, 'application/pdf')
        }

        response = requests.post(upload_url, files=files)
        
        if response.status_code in [200, 201, 204]:
            # File uploaded successfully, extract the file ID from the response
            file_id = response.json().get("id")
            return file_id
        else:
            print(f"Failed to upload the file. Status code: {response.status_code}, Response: {response.text}")
            return None

# Step 3: Submit the assignment with the uploaded file
def submit_assignment_with_file(course_id, assignment_id, file_id):
    url = f"{BASE_URL}/courses/{course_id}/assignments/{assignment_id}/submissions"

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "submission": {
            "submission_type": "online_upload",
            "file_ids": [file_id]  # List of file IDs
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 201:
        print("Assignment submitted successfully!")
    else:
        print(f"Failed to submit assignment. Status code: {response.status_code}, Response: {response.text}")


# Run the steps to upload the file and submit it
upload_url, file_param = start_file_upload(COURSE_ID, PDF_FILE_PATH)

if upload_url and file_param:
    file_id = upload_file(upload_url, file_param, PDF_FILE_PATH)

    if file_id:
        submit_assignment_with_file(COURSE_ID, ASSIGNMENT_ID, file_id)