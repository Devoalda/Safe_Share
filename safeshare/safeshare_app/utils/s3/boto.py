import os
import boto3
from dotenv import load_dotenv

def initialize_s3_client():
    # Load environment variables from .env file
    load_dotenv()

    # Access AWS credentials
    aws_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    # Initialize and return the S3 client
    return boto3.client(
        's3',
        aws_access_key_id = aws_key,
        aws_secret_access_key = aws_secret_key
    )

def upload_file_to_s3(client, file_path, bucket_name, object_name):
    with open(file_path, "rb") as file:
        client.upload_fileobj(file, bucket_name, object_name)

def download_file_from_s3(client, bucket_name, object_name, file_path):
    with open(file_path, 'wb') as file:
        client.download_fileobj(bucket_name, object_name, file)


# create main function
if __name__ == "__main__":  
    
    client = initialize_s3_client()
    
    upload_file_to_s3(client, "C:/Users/lowho/OneDrive/Desktop/Y2T1/Embedded Systems/magnetometer.pdf", "cloud-computing-team16", "upload.pdf")
    
    # the file name has to be unique else will have issue
    download_file_from_s3(client, "cloud-computing-team16", "upload.pdf", "C:/Users/lowho/OneDrive/Desktop/Y2T1/Embedded Systems/new_magnetometer.pdf")
