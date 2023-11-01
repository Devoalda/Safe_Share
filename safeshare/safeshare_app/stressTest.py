import concurrent.futures
import io
import random
import string

import requests

# Endpoint
endpoint_url = "http://IP:PORT/api/files/" # Change IP and PORT as needed

# Number of files to send
num_files = 3
num_threads = 5  # Change the number of threads as needed

# Test file path
test_file_path = "/path/to/virus.exe"


# Function to generate random file content
def generate_random_content():
    content_length = random.randint(1024, 20480)  # Random content size between 1KB and 20KB
    return ''.join(random.choices(string.ascii_letters + string.digits, k=content_length))


# Function to send files in a thread and return the key
def send_files_thread(thread_id, use_test_file=False):
    keys = []
    for i in range(num_files):
        if use_test_file and i == 0:
            # Send the test file
            with open(test_file_path, 'rb') as test_file:
                test_file_content = io.BytesIO(test_file.read())
                files = {'file': ('shell_reverse.exe', test_file_content)}
        else:
            # Generate random file content
            content = generate_random_content()
            file_content = io.BytesIO(content.encode())
            files = {'file': ('file{}.txt'.format(i), file_content)}

        # Define any additional data you want to send with the request
        data = {'ttl': 60}

        try:
            # Make the POST request
            response = requests.post(endpoint_url, files=files, data=data)

            # Check if the request was successful
            if response.status_code == 201:
                items = response.json()
                for item in items:
                    key = item.get('key')
                    if key:
                        keys.append(key)
                        print(f"Thread {thread_id}: File {i} uploaded successfully with key {key}.")
                    else:
                        print(f"Thread {thread_id}: File {i} uploaded, but key not found in the response.")
            else:
                print(f"Thread {thread_id}: File {i} upload failed with status code {response.status_code}.")
        except Exception as e:
            print(f"Thread {thread_id}: An error occurred while sending file {i}: {str(e)}")
        finally:
            # Close the file content
            if use_test_file:
                test_file_content.close()
            else:
                file_content.close()

    return keys


# Function to receive files in a thread using the provided key
def receive_files_thread(thread_id, file_key):
    try:
        # Make the GET request to retrieve the file using the provided key
        response = requests.get(endpoint_url + file_key)

        # Check if the request was successful
        if response.status_code == 200:
            # Save or process the received file content here
            print(f"Thread {thread_id}: File with key {file_key} received successfully.")
        else:
            print(
                f"Thread {thread_id}: File with key {file_key} retrieval failed with status code {response.status_code}.")
    except Exception as e:
        print(f"Thread {thread_id}: An error occurred while receiving the file with key {file_key}: {str(e)}")


# Create and send/receive files using multiple threads
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    # Select a random subset of threads to use the test file
    use_test_file_threads = random.sample(range(num_threads), min(num_threads, num_files))

    # Start multiple threads for sending files
    send_futures = []
    for thread_id in range(num_threads):
        use_test_file = thread_id in use_test_file_threads
        future = executor.submit(send_files_thread, thread_id, use_test_file)
        send_futures.append(future)

    # Retrieve the keys from the responses
    keys = []
    for future in concurrent.futures.as_completed(send_futures):
        keys.extend(future.result())

    # Start multiple threads for receiving files using the obtained keys
    receive_futures = [executor.submit(receive_files_thread, thread_id, file_key) for thread_id, file_key in
                       enumerate(keys) if file_key]

    # Wait for all receive threads to complete
    concurrent.futures.wait(receive_futures)
