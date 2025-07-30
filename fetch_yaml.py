import requests
import sys
import os

# GitHub repository configuration
REPO_USER = "4D4937"
REPO_NAME = "k8s"
REPO_BRANCH = "main"

def list_yaml_files():
    api_url = f"https://api.github.com/repos/{REPO_USER}/{REPO_NAME}/contents?ref={REPO_BRANCH}"
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

def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("  python3 fetch_yaml.py <file.yaml>   # Download a YAML file")
        print("  python3 fetch_yaml.py list          # List available YAML files")
        sys.exit(1)

    arg = sys.argv[1]
    if arg == "list":
        list_yaml_files()
    else:
        download_yaml(arg)

if __name__ == "__main__":
    main()
