import requests
import io
import os

# Endpoint
endpoint_url = "http://127.0.0.1:8000/api/files/"

# Number of files to send
num_files = 5

# Create and send files
for i in range(num_files):
    # Generate sample file
    file_content = io.BytesIO(b'This is a sample file content.')

    # Define the files dictionary for the POST request
    files = {'file': ('file{}.txt'.format(i), file_content)}

    # Define any additional data you want to send with the request
    data = {'ttl': 60}

    # Make the POST request
    response = requests.post(endpoint_url, files=files, data=data)

    # Check if the request was successful
    if response.status_code == 201:
        print(f"File {i} uploaded successfully.")
    else:
        print(f"File {i} upload failed with status code {response.status_code}.")

    # Close the file content
    file_content.close()
