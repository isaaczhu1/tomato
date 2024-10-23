import requests

# Canvas API settings
API_URL = "https://canvas.mit.edu/api/v1"
ACCESS_TOKEN = "7867~F9HUWP7eLKL8a9nzMUtwLv6PtUAWELezkr9KDKWCa6nFQYzX22G4HNJCJmAQCTLU"
def get_course_files(course_id):
    """
    Lists all files in the specified Canvas course.
    
    Parameters:
    course_id (int): The Canvas course ID.
    
    Returns:
    list: A list of file metadata for each file in the course.
    """
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    # Make the API request to list all files in the course
    response = requests.get(f"{API_URL}/courses/{course_id}/files", headers=headers)
    
    if response.status_code == 200:
        files = response.json()
        return files
    else:
        print(f"Error: Failed to get files for course (Status code {response.status_code})")
        print("Response:", response.text)
        return None

def find_file_by_page_id(files, page_file_id):
    """
    Searches for a file in the list of files based on the Canvas file page ID.
    
    Parameters:
    files (list): List of files returned from the Canvas API.
    page_file_id (int): The file ID from the Canvas URL (not the API file ID).
    
    Returns:
    dict: The matching file metadata or None if not found.
    """
    # Look for the file with the matching page file ID
    for file in files:
        if str(page_file_id) in file.get('url', ''):  # Check if the page ID is in the file URL
            return file
    return None

if __name__ == "__main__":
    # Example: URL https://canvas.mit.edu/courses/28240/files/4521000
    course_id = "28240"  # Replace with your actual course ID
    page_file_id = "4521000"  # This is the file ID in the URL
    
    # Step 1: Get all files for the course
    files = get_course_files(course_id)
    
    if files:
        # Step 2: Find the actual file metadata by matching the page ID
        file_metadata = find_file_by_page_id(files, page_file_id)
        
        if file_metadata:
            # Print the actual file ID and other details
            print(f"Found file: {file_metadata['display_name']}")
            print(f"Actual File ID: {file_metadata['id']}")
            print(f"Download URL: {file_metadata['url']}")
        else:
            print("File not found based on the page file ID.")