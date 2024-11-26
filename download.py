import requests
import os

# get the environment variables $CANVAS_BASE and $CANVAS_TOKEN from the shell
# Canvas API settings
API_URL = os.getenv("CANVAS_BASE")
ACCESS_TOKEN = os.getenv("CANVAS_TOKEN")

if not API_URL or not ACCESS_TOKEN:
    raise EnvironmentError("Please set the CANVAS_BASE and CANVAS_TOKEN environment variables.")


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

def find_actual_file_id(course_id, file_name):
    """
    Finds the actual file ID for a file in a course by matching the file name.
    
    Parameters:
    course_id (str): The Canvas course ID.
    file_name (str): The name of the file to search for.
    
    Returns:
    str: The actual file ID if found, None otherwise.
    """
    files = list_course_files(course_id)
    
    if files:
        for file in files:
            if file.get('display_name') == file_name:
                return file.get('id')
        print(f"Error: File '{file_name}' not found in the course.")
        return None
    else:
        return None

def get_file_metadata(file_id):
    """
    Retrieves the metadata for a file from the Canvas API using the file ID.
    
    Parameters:
    file_id (str): The Canvas file ID.
    
    Returns:
    dict: The file metadata, including the download URL, if found.
    """
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    # Make an API request to get the file details
    response = requests.get(f"{API_URL}/files/{file_id}", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Failed to get file metadata (Status code {response.status_code})")
        return None

def download_canvas_file(download_url, output_directory, output_filename):
    """
    Downloads a file from Canvas using the download URL and saves it to a specified directory.
    
    Parameters:
    download_url (str): The authenticated URL to download the file.
    output_directory (str): The directory where the file should be saved.
    output_filename (str): The name of the file to save the download as.
    """
    response = requests.get(download_url, stream=True)
    
    if response.status_code == 200:
        # Ensure the output directory exists
        os.makedirs(output_directory, exist_ok=True)
        
        # Construct the full path for the output file
        output_path = os.path.join(output_directory, output_filename)
        
        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"File downloaded successfully as {output_path}")
    else:
        print(f"Error: Failed to download file (Status code {response.status_code})")

def download_file(actual_file_id, output_directory, output_filename=None):
    """
    Downloads a file from Canvas using the file ID and saves it to a specified directory.
    
    Parameters:
    actual_file_id (str): The Canvas file ID.
    output_directory (str): The directory where the file should be saved.
    output_filename (str, optional): The name of the file to save the download as. If not provided, the original file name will be used.
    """
    # Step 1: Retrieve the file metadata from the Canvas API
    file_metadata = get_file_metadata(actual_file_id)
    
    if file_metadata:
        # Step 2: Use the download URL from the metadata to download the file
        download_url = file_metadata.get('url')
        original_file_name = file_metadata.get('display_name', 'downloaded_file')

        if download_url:
            # Step 3: Download the file and save it with the appropriate name
            final_file_name = output_filename if output_filename else original_file_name
            download_canvas_file(download_url, output_directory, final_file_name)
        else:
            print("Error: Download URL not found in file metadata.")


if __name__ == "__main__":
    # Replace this with the actual file ID you retrieved
    # pass
    actual_file_id = find_actual_file_id("28240", "ps4.pdf")
    print(actual_file_id)
    # download it and put it in psets/pset4/ directory, renaming it to problemset4.pdf
    download_file(actual_file_id, "psets/pset4", "problemset4.pdf")