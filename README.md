# yaml-fetcher

A simple Python tool to list and download `.yaml` or `.yml` files from a GitHub repository — no cloning, no execution.

## Features

- 🔍 List all `.yaml` / `.yml` files in a GitHub repository  
- ⬇️ Download a specific YAML file to the current directory  
- ❌ No repository cloning required  
- 🛡️ Does **not** execute any file — safe for use in automation  

## Usage

### 1. List available YAML files

```bash
python3 fetch_yaml.py list
```

### 2. Download a YAML file

```bash
python3 fetch_yaml.py <filename.yaml>
```

**Example:**

```bash
python3 fetch_yaml.py k8s-deployment.yaml
```

## Configuration

Edit the following lines at the top of `fetch_yaml.py` to point to your desired repository:

```python
REPO_USER = "4D4937"
REPO_NAME = "k8s"
REPO_BRANCH = "main"
```

## Requirements

- Python 3.x  
- [`requests`](https://pypi.org/project/requests/) library

Install the required dependency:

```bash
pip install requests
```

## License

[MIT](LICENSE)
