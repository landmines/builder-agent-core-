import os
import requests
from base64 import b64encode

def push_to_github(task):
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise Exception("Missing GITHUB_TOKEN in Replit secrets")

    repo_url = task.get("repo")
    commit_message = task.get("commit_message", "Automated push from Builder Agent")
    filename_single = task.get("filename")

    # Determine repo owner and name from URL
    try:
        parts = repo_url.rstrip("/").split("/")
        repo_owner = parts[-2]
        repo_name = parts[-1]
    except Exception:
        raise Exception("Invalid repo URL")

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Multi-file support
    files = task.get("files", [])
    if not files and filename_single:
        files = [{"local_path": filename_single, "repo_path": filename_single}]

    results = []

    for file in files:
        local_path = file.get("local_path")
        repo_path = file.get("repo_path", local_path)

        if not os.path.exists(local_path):
            print(f"[!] File not found: {local_path}")
            results.append(f"File not found: {local_path}")
            continue

        with open(local_path, "rb") as f:
            content = f.read()

        encoded = b64encode(content).decode("utf-8")

        # Check if file exists (to get sha)
        get_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{repo_path}"
        get_resp = requests.get(get_url, headers=headers)

        sha = None
        if get_resp.status_code == 200:
            sha = get_resp.json().get("sha")

        payload = {
            "message": commit_message,
            "content": encoded,
            "branch": task.get("branch", "main")
        }
        if sha:
            payload["sha"] = sha

        put_resp = requests.put(get_url, headers=headers, json=payload)

        if put_resp.status_code in [200, 201]:
            print(f"[+] {local_path} pushed as {repo_path}")
            results.append(f"Pushed {repo_path}")
        else:
            error = put_resp.json().get("message", "Unknown error")
            print(f"[!] Failed to push {repo_path}: {error}")
            results.append(f"Failed to push {repo_path}: {error}")

    return results