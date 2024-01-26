import os
import requests
import json

# API Gateway endpoint for the uploader Lambda
api_url = "https://5cg3yb27k0.execute-api.ap-south-1.amazonaws.com/Stage/lambda-function-1"

# Path to the folder containing images
folder_path = r"G:\3gi\kagglecatsanddogs_5340\Pets"

# List all .jpg files recursively in the folder
file_list = [os.path.join(dirpath, filename) for dirpath, _, filenames in os.walk(folder_path) for filename in filenames if filename.endswith('.jpg')]

# Prepare payload
payload = {"files": file_list}

# Send a POST request to the API Gateway
response = requests.post(api_url, data=json.dumps(payload))

try:
    # Extract the list of presigned URLs from the response
    presigned_urls = response.json()["presigned_urls"]

    # Upload each file to S3 using the presigned URLs
    for file_name, presigned_url in zip(file_list, presigned_urls):
        with open(file_name, "rb") as file:
            upload_response = requests.put(presigned_url, data=file)

        # Handle the upload_response
        if upload_response.status_code == 200:
            print(f"File {file_name} uploaded successfully.")
        else:
            print(f"Failed to upload {file_name}. Status code: {upload_response.status_code}")

except json.JSONDecodeError:
    print("Error decoding JSON response from the API.")

except KeyError:
    print("Response does not contain the expected 'presigned_urls' field.")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
