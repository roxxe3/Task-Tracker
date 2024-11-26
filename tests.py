import unittest
import json
import os
from task_tracker import Task


class TestTaskCLI(unittest.TestCase):

    def setUp(self):
        """Setup a temporary JSON file for testing."""
        self.test_file = 'test_data.json'
        with open(self.test_file, 'w') as file:
            json.dump([], file, indent=4)
        self.original_file = Task.__dict__.get('file_name', 'data.json')
        Task.file_name = self.test_file

    def tearDown(self):
        """Clean up the test file after each test."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_task(self):
        """Test adding a task."""
        task = Task("Test Task", "todo")
        task.add_task()

        with open(self.test_file, 'r') as file:
            data = json.load(file)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["description"], "Test Task")
        self.assertEqual(data[0]["status"], "todo")

    def test_update_task(self):
        """Test updating a task's description."""
        task = Task("Old Description", "todo")
        task.add_task()
        task_id = str(task.id)

        Task.update_task(task_id, "New Description")

        with open(self.test_file, 'r') as file:
            data = json.load(file)

        self.assertEqual(data[0]["description"], "New Description")

    def test_delete_task(self):
        """Test deleting a task."""
        task = Task("Task to Delete", "todo")
        task.add_task()
        task_id = str(task.id)

        Task.delete_task(task_id)

        with open(self.test_file, 'r') as file:
            data = json.load(file)

        self.assertEqual(len(data), 0)

    def test_mark_in_progress(self):
        """Test marking a task as in progress."""
        task = Task("Task to Mark", "todo")
        task.add_task()
        task_id = str(task.id)

        Task.mark_in_progress("mark-in-progress", task_id)

        with open(self.test_file, 'r') as file:
            data = json.load(file)

        self.assertEqual(data[0]["status"], "in progress")

    def test_list_tasks(self):
        """Test listing tasks."""
        task1 = Task("Task 1", "todo")
        task2 = Task("Task 2", "in progress")
        task1.add_task()
        task2.add_task()

        with open(self.test_file, 'r') as file:
            data = json.load(file)

        self.assertEqual(len(data), 2)

        # Simulate listing with a status filter
        filtered_tasks = [t for t in data if t["status"] == "todo"]
        self.assertEqual(len(filtered_tasks), 1)
        self.assertEqual(filtered_tasks[0]["description"], "Task 1")


if __name__ == "__main__":
    unittest.main()
