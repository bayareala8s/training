import urllib.request
import urllib.parse
import urllib.error
import boto3

# S3 Configuration
S3_BUCKET = "your-bucket-name"  # Replace with your actual S3 bucket name
BASE_URL = "https://download.bls.gov/pub/time.series/"

def list_files_and_dirs(url):
    """ Fetch and parse directory listing for both files and subdirectories """
    try:
        with urllib.request.urlopen(url) as response:
            html_content = response.read().decode("utf-8")

        file_list = []
        dir_list = []

        for line in html_content.split("\n"):
            if 'href="' in line:
                start = line.find('href="') + len('href="')
                end = line.find('"', start)
                item = line[start:end]

                if item == "../":  # Ignore parent directory reference
                    continue
                
                if item.endswith("/"):  # It's a subdirectory
                    dir_list.append(item)
                else:  # It's a file
                    file_list.append(item)

        return file_list, dir_list

    except urllib.error.URLError as e:
        print(f"Failed to fetch directory list from {url}: {e}")
        return [], []

def download_file(url):
    """ Download file content """
    try:
        with urllib.request.urlopen(url) as response:
            return response.read()
    except urllib.error.URLError as e:
        print(f"Failed to download {url}: {e}")
        return None

def upload_to_s3(file_key, content):
    """ Upload file content to S3 preserving folder structure """
    try:
        s3_client = boto3.client("s3")
        s3_client.put_object(Bucket=S3_BUCKET, Key=file_key, Body=content)
        print(f"Uploaded: {file_key}")
    except Exception as e:
        print(f"Failed to upload {file_key}: {e}")

def traverse_and_download(base_url, prefix=""):
    """ Recursively traverse directories and download files """
    files, directories = list_files_and_dirs(base_url)

    # Process files in the current directory
    for file_name in files:
        file_url = base_url + file_name
        file_key = prefix + file_name  # Maintain directory structure in S3

        file_content = download_file(file_url)
        if file_content is not None:
            upload_to_s3(file_key, file_content)

    # Recursively process subdirectories
    for directory in directories:
        traverse_and_download(base_url + directory, prefix + directory)

def lambda_handler(event, context):
    """ AWS Lambda entry function """
    traverse_and_download(BASE_URL)
    print("All files downloaded and uploaded successfully.")
