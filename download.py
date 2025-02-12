import urllib.request
import os

# HTTPS Proxy details (Replace with your proxy)
PROXY_URL = "https://your-proxy-ip:your-proxy-port"
PROXY_USER = "your-username"
PROXY_PASS = "your-password"

# Target URL
TARGET_URL = "https://download.bls.gov/pub.time.series/"

# Custom headers to mimic a browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://download.bls.gov/",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
}

# Create a proxy handler
proxy_handler = urllib.request.ProxyHandler({
    "https": PROXY_URL
})

# Add authentication (if required)
if PROXY_USER and PROXY_PASS:
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, PROXY_URL, PROXY_USER, PROXY_PASS)
    auth_handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(proxy_handler, auth_handler)
else:
    opener = urllib.request.build_opener(proxy_handler)

# Set the global opener
urllib.request.install_opener(opener)

def fetch_url(url):
    """ Fetch URL through the proxy """
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req) as response:
            return response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        print(f"⚠️ HTTP Error {e.code}: {url}")
    except urllib.error.URLError as e:
        print(f"⚠️ URL Error: {e}")
    return None

def lambda_handler(event, context):
    """ AWS Lambda Entry Point """
    print(f"Connecting to {TARGET_URL} through proxy {PROXY_URL}")

    response_content = fetch_url(TARGET_URL)
    if response_content:
        print("✅ Successfully fetched data!")
    else:
        print("⚠️ Failed to retrieve data.")

    return {"statusCode": 200, "body": "Proxy test complete"}
