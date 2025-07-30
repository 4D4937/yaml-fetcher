# fetch_yaml

A simple Python CLI tool (and compiled binary) to **list**, **download**, and **upload** `.yaml` files to a GitHub repository — no git cloning required.

> Includes a GitHub Actions workflow to build a standalone binary with an embedded GitHub token.

---

## ✨ Features

- ✅ List all `.yaml` / `.yml` files in a public GitHub repo
- ✅ Download a specific YAML file from the repo
- ✅ Upload a local YAML file to the repo (token is embedded in the binary)
- ✅ Build a portable binary using PyInstaller + GitHub Actions

---

## 🧩 Usage

### 🔍 List YAML files

```bash
python3 fetch_yaml.py list
```

### 📥 Download a YAML file

```bash
python3 fetch_yaml.py <filename.yaml>
```

Example:

```bash
python3 fetch_yaml.py nginx-deployment.yaml
```

### 📤 Upload a YAML file (binary includes token)

```bash
./fetch_yaml upload ./local-file.yaml [remote-name.yaml]
```

If `remote-name` is omitted, it uses the local filename.

---

## 🔐 Token Injection

This tool embeds a GitHub token at compile time.

To securely inject your token:

1. Generate a GitHub [Personal Access Token](https://github.com/settings/tokens) with `repo` scope.
2. Add it as a GitHub Secret named `YAML_PUSH_TOKEN`.
3. Run the provided GitHub Actions workflow.

---

## 🛠 GitHub Actions Build

The build workflow:

- Replaces the `{{GITHUB_TOKEN}}` placeholder in `fetch_yaml.py`
- Compiles it using PyInstaller in Docker
- Uploads the resulting binary as an artifact

See the workflow file:

```
.github/workflows/build.yml
```

To trigger it, go to **GitHub → Actions → Run workflow**.

---

## 📦 Requirements (for Python usage)

- Python 3.x
- `requests` library

Install dependencies:

```bash
pip install requests
```

---

## 🔧 Repository Configuration

Repository is hardcoded in `fetch_yaml.py`. You can change:

```python
REPO_USER = "4D4937"
REPO_NAME = "k8s"
REPO_BRANCH = "main"
```

---

## ⚠️ Disclaimer

> This tool embeds a GitHub token in the binary. **Do not** distribute it publicly unless you fully understand the risks.

---

## 📝 License

MIT
