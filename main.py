from task_loader import load_tasks
from agent_executor import execute_task
from logger import log_result

def main():
    print("== Builder Agent Activated ==")
    tasks = load_tasks("task.json")

    for i, task in enumerate(tasks):
        print(f"\n>> Executing Task {i+1}: {task.get('type')}")
        result = execute_task(task)
        log_result(task, result)

if __name__ == "__main__":
    main()