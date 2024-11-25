import subprocess
from unittest.mock import patch

def test_cli_help():
    # Simulate running the CLI with "--help" flag
    result = subprocess.run(["python3", "task_tracker.py", "--help"], capture_output=True, text=True)
    assert "usage" in result.stdout

def test_cli_add_task():
    # Mock input() to simulate the user adding a task
    with patch("builtins.input", side_effect=["Test Task"]):
        result = subprocess.run(["python3", "task_tracker.py", "add"], capture_output=True, text=True)
        assert "Task added" in result.stdout
