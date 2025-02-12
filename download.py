import urllib.request
import urllib.error
import http.cookiejar
import os
import time

# AWS Lambda: Save to /tmp (Lambda has only 512MB disk space in /tmp)
LOCAL_SAVE_PATH = "/tmp/bls_time_series"
BASE_URL = "https://download.bls.gov/pub.time.series/"

# Create a CookieJar to store cookies
cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

# Custom headers to mimic a real browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://download.bls.gov/",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
}

def make_request(url):
    """ Make a request with proper headers and session handling """
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        response = opener.open(req)
        return response.read()
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(f"⚠️ HTTP 403 Forbidden: Blocked for {url}. Retrying with delay...")
            time.sleep(5)
            return None
        else:
            print(f"⚠️ HTTP Error {e.code} for {url}")
            return None
    except urllib.error.URLError as e:
        print(f"⚠️ URL Error: {e}")
        return None

def list_files_and_folders(url):
    """ Fetch directory listing and extract file names """
    try:
        print(f"Accessing: {url}")
        html_content = make_request(url)
        if not html_content:
            return []

        # Extract href links (filenames + folders)
        pattern = r'href="([^"]+)"'
        entries = re.findall(pattern, html_content.decode("utf-8"))

        # Remove "../" and other navigation links
        valid_entries = [entry for entry in entries if not entry.startswith("../")]

        print(f"Found: {valid_entries}")
        return valid_entries

    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")
        return []

def download_file(url, save_path):
    """ Download file and save to AWS Lambda /tmp directory """
    try:
        print(f"Downloading: {url}")
        file_content = make_request(url)

        if not file_content:
            print(f"⚠️ Skipping {url} due to error.")
            return

        # Ensure local directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Save file to /tmp/
        with open(save_path, "wb") as file:
            file.write(file_content)

        print(f"✅ Saved: {save_path}")

    except Exception as e:
        print(f"⚠️ Error downloading {url}: {e}")

def process_directory(base_url, relative_path=""):
    """ Recursively process directories and download all files """
    current_url = base_url + relative_path
    entries = list_files_and_folders(current_url)

    for entry in entries:
        entry_url = current_url + entry
        entry_relative_path = os.path.join(relative_path, entry)  # Maintain directory structure
        local_file_path = os.path.join(LOCAL_SAVE_PATH, entry_relative_path)

        if entry.endswith("/"):  # It's a subdirectory
            time.sleep(1)  # Avoid rate-limiting
            process_directory(base_url, entry_relative_path)  # Recurse into subdirectory
        else:  # It's a file
            download_file(entry_url, local_file_path)

def lambda_handler(event, context):
    """ AWS Lambda entry point """
    print(f"Starting download from {BASE_URL}")
    process_directory(BASE_URL)
    print("Download completed.")
