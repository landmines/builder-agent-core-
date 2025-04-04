import subprocess
from gpt_handler import generate_code
from github_ops import push_to_github

def execute_task(task):
    task_type = task.get("type")

    if task_type == "codegen":
        filename = task["filename"]
        code = task["code"] or generate_code(task.get("prompt", ""))
        with open(filename, "w") as f:
            f.write(code)
        print(f"[+] Code written to {filename}")
        return f"Code written to {filename}"

    elif task_type == "run":
        file = task["file"]
        try:
            print(f"[~] Running {file}...")
            result = subprocess.run(["python", file], capture_output=True, text=True)
            print(result.stdout)
            print(result.stderr)
            return result.stdout or result.stderr
        except Exception as e:
            return f"[!] Execution failed: {e}"

    elif task_type == "push":
        try:
            print("[~] Attempting GitHub push...")
            result = push_to_github(task)
            print("[+] GitHub push complete")
            return result
        except Exception as e:
            print(f"[!] GitHub push failed: {e}")
            return f"GitHub push failed: {e}"

    else:
        return f"[!] Unknown task type: {task_type}"