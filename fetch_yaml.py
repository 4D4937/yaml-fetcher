import requests
import sys
import os
import base64

# GitHub repository configuration
REPO_USER = "4D4937"
REPO_NAME = "k8s"
REPO_BRANCH = "main"
GITHUB_API = "https://api.github.com"

# Token placeholder - will be replaced at build time by GitHub Actions
GITHUB_TOKEN = "{{GITHUB_TOKEN}}"

def list_yaml_files():
    api_url = f"{GITHUB_API}/repos/{REPO_USER}/{REPO_NAME}/contents?ref={REPO_BRANCH}"
    response = requests.get(api_url)

    if response.status_code == 200:
        print("Available YAML files in the repository:")
        for item in response.json():
            if item['type'] == 'file' and item['name'].endswith((".yaml", ".yml")):
                print(f"  - {item['name']}")
    else:
        print(f"Failed to fetch file list (HTTP {response.status_code})")

def download_yaml(script_name):
    if not script_name.endswith((".yaml", ".yml")):
        print("Error: Only .yaml or .yml files can be downloaded.")
        return

    url = f"https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/{REPO_BRANCH}/{script_name}"
    print(f"Downloading: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        with open(script_name, "w") as f:
            f.write(response.text)
        print(f"File saved as: {script_name}")
    else:
        print(f"Error: File '{script_name}' not found (HTTP {response.status_code}).")

def upload_yaml(local_path, remote_name=None):
    if not GITHUB_TOKEN or GITHUB_TOKEN.startswith("{{"):
        print("Error: GITHUB_TOKEN is not set or not replaced.")
        return

    if not os.path.isfile(local_path):
        print(f"Error: File '{local_path}' does not exist.")
        return

    if not local_path.endswith((".yaml", ".yml")):
        print("Error: Only .yaml or .yml files can be uploaded.")
        return

    remote_name = remote_name or os.path.basename(local_path)

    with open(local_path, "rb") as f:
        content = f.read()
    encoded = base64.b64encode(content).decode("utf-8")

    url = f"{GITHUB_API}/repos/{REPO_USER}/{REPO_NAME}/contents/{remote_name}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    # Check if file already exists
    get_resp = requests.get(url, headers=headers)
    sha = get_resp.json().get("sha") if get_resp.status_code == 200 else None

    data = {
        "message": f"Upload {remote_name}",
        "branch": REPO_BRANCH,
        "content": encoded,
    }
    if sha:
        data["sha"] = sha

    resp = requests.put(url, json=data, headers=headers)
    if resp.status_code in (200, 201):
        print(f"✅ Uploaded: {remote_name}")
    else:
        print(f"❌ Upload failed: {resp.status_code}")
        print(resp.json())

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 fetch_yaml.py list")
        print("  python3 fetch_yaml.py <file.yaml>         # Download")
        print("  python3 fetch_yaml.py upload <local_file> [remote_name]  # Upload")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "list":
        list_yaml_files()
    elif cmd == "upload" and len(sys.argv) >= 3:
        upload_yaml(sys.argv[2], sys.argv[3] if len(sys.argv) >= 4 else None)
    else:
        download_yaml(cmd)

if __name__ == "__main__":
    main()
