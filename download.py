import urllib.request
import urllib.parse
import urllib.error
import boto3

# S3 Configuration
S3_BUCKET = "your-bucket-name"  # Replace with your actual S3 bucket name
BASE_URL = "https://download.bls.gov/pub/time.series/"  # Root URL

def list_files_and_folders(url):
    """ Fetch and parse directory listing from a web directory, handling subdirectories """
    try:
        with urllib.request.urlopen(url) as response:
            html_content = response.read().decode("utf-8")

        # Extract file and folder names
        entries = []
        for line in html_content.split("\n"):
            if 'href="' in line:
                start = line.find('href="') + len('href="')
                end = line.find('"', start)
                name = line[start:end]

                # Ignore parent directory reference
                if not name.startswith("../"):
                    entries.append(name)

        return entries

    except urllib.error.URLError as e:
        print(f"Failed to fetch directory listing from {url}: {e}")
        return []

def download_file(url):
    """ Download file content """
    try:
        with urllib.request.urlopen(url) as response:
            return response.read()
    except urllib.error.URLError as e:
        print(f"Failed to download {url}: {e}")
        return None

def upload_to_s3(s3_path, content):
    """ Upload file content to S3 """
    try:
        s3_client = boto3.client("s3")
        s3_client.put_object(Bucket=S3_BUCKET, Key=s3_path, Body=content)
        print(f"Uploaded: {s3_path}")
    except Exception as e:
        print(f"Failed to upload {s3_path}: {e}")

def process_directory(base_url, relative_path=""):
    """ Recursively process directories and upload files while preserving structure """
    current_url = base_url + relative_path
    entries = list_files_and_folders(current_url)

    for entry in entries:
        entry_url = current_url + entry
        entry_relative_path = relative_path + entry

        if entry.endswith("/"):  # It's a subdirectory
            process_directory(base_url, entry_relative_path)  # Recursively process subdirectory
        else:  # It's a file
            file_content = download_file(entry_url)
            if file_content:
                upload_to_s3(entry_relative_path, file_content)

def lambda_handler(event, context):
    """ AWS Lambda main function """
    print(f"Starting download from {BASE_URL}")
    process_directory(BASE_URL)
    print("Download and upload completed.")
