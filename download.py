import urllib.request
import urllib.error
import os
import re
import time

# Get the user's Downloads folder path
LOCAL_DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads", "bls_time_series")

# Base URL to scrape files from
BASE_URL = "https://download.bls.gov/pub/time.series/"

def list_files_and_folders(url):
    """ Fetch directory listing and extract file names and subdirectories """
    try:
        print(f"Accessing: {url}")
        with urllib.request.urlopen(url) as response:
            html_content = response.read().decode("utf-8")

        # Extract href links that contain filenames and directories
        pattern = r'href="([^"]+)"'
        entries = re.findall(pattern, html_content)

        # Filter out navigation links (../) and invalid entries
        valid_entries = [entry for entry in entries if not entry.startswith("../")]

        print(f"Found: {valid_entries}")  # Debugging
        return valid_entries

    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code} while accessing {url}")
        return []
    except urllib.error.URLError as e:
        print(f"URL Error while accessing {url}: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error while accessing {url}: {e}")
        return []

def download_file(url, save_path):
    """ Download file and save it locally in the Downloads folder """
    try:
        print(f"Downloading: {url}")
        with urllib.request.urlopen(url) as response:
            file_content = response.read()
        
        # Ensure local directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Save file locally
        with open(save_path, "wb") as file:
            file.write(file_content)
        
        print(f"Saved: {save_path}")
    except urllib.error.HTTPError as e:
        print(f"Failed to download {url} - HTTP Error {e.code}")
    except urllib.error.URLError as e:
        print(f"Failed to download {url} - URL Error: {e}")

def process_directory(base_url, relative_path=""):
    """ Recursively process directories and download all files """
    current_url = base_url + relative_path
    entries = list_files_and_folders(current_url)

    for entry in entries:
        entry_url = current_url + entry
        entry_relative_path = os.path.join(relative_path, entry)  # Maintain directory structure
        local_file_path = os.path.join(LOCAL_DOWNLOADS_FOLDER, entry_relative_path)

        if entry.endswith("/"):  # It's a subdirectory
            time.sleep(1)  # Add delay to prevent rate limiting
            process_directory(base_url, entry_relative_path)  # Recurse into subdirectory
        else:  # It's a file
            download_file(entry_url, local_file_path)

def main():
    """ Main function to start downloading """
    print(f"Starting download from {BASE_URL}")
    process_directory(BASE_URL)
    print(f"All files have been saved in: {LOCAL_DOWNLOADS_FOLDER}")

if __name__ == "__main__":
    main()
