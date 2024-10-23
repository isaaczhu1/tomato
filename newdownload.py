import requests
from bs4 import BeautifulSoup

# Canvas API settings
API_URL = "https://canvas.mit.edu/api/v1"
ACCESS_TOKEN = "7867~F9HUWP7eLKL8a9nzMUtwLv6PtUAWELezkr9KDKWCa6nFQYzX22G4HNJCJmAQCTLU"

def list_course_files(course_id):
    """
    Lists all files in a course using the Canvas API.
    
    Parameters:
    course_id (str): The Canvas course ID.
    
    Returns:
    list: A list of file metadata for all files in the course.
    """
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    files = []
    url = f"{API_URL}/courses/{course_id}/files"
    
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            files.extend(response.json())
            # Check for pagination
            if 'next' in response.links:
                url = response.links['next']['url']
            else:
                url = None
        else:
            print(f"Error: Failed to list files (Status code {response.status_code})")
            return None

    return files


files = list_course_files("28240")
print(files)