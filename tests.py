import unittest
import json
import os
from datetime import datetime
from unittest.mock import patch
from task_tracker import Task

class TestTaskTracker(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_file = "test_data.json"
        # Ensure clean state before each test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def tearDown(self):
        """Clean up after each test method."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_task_creation(self):
        """Test that a task is created with correct attributes."""
        task = Task("Test task", "todo", self.test_file)
        self.assertIsNotNone(task.id)
        self.assertEqual(task.description, "Test task")
        self.assertEqual(task.status, "todo")
        self.assertIsInstance(task.createdAt, datetime)
        self.assertIsInstance(task.updatedAt, datetime)

    def test_add_task(self):
        """Test adding a task to the JSON file."""
        task = Task("Test task", "todo", self.test_file)
        task.add_task()
        
        # Verify task was written to file
        with open(self.test_file, 'r') as file:
            data = json.load(file)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["description"], "Test task")
        self.assertEqual(data[0]["status"], "todo")

    def test_update_task(self):
        """Test updating an existing task."""
        # First create a task
        task = Task("Original task", "todo", self.test_file)
        task.add_task()
        task_id = str(task.id)
        
        # Update the task
        Task.update_task(task_id, "Updated task", self.test_file)
        
        # Verify update
        with open(self.test_file, 'r') as file:
            data = json.load(file)
        
        self.assertEqual(data[0]["description"], "Updated task")

    @patch('builtins.print')
    def test_delete_task(self, mock_print):
        """Test deleting a task."""
        task = Task("Task to delete", "todo", self.test_file)
        task.add_task()
        task_id = str(task.id)
        
        Task.delete_task(task_id, self.test_file)
        
        with open(self.test_file, 'r') as file:
            data = json.load(file)
        
        self.assertEqual(len(data), 0)

    def test_mark_in_progress(self):
        """Test marking a task as in progress."""
        # Create a task
        task = Task("Test task", "todo", self.test_file)
        task.add_task()
        task_id = str(task.id)
        
        # Mark as in progress
        Task.mark_in_progress(task_id, self.test_file)
        
        # Verify status change
        with open(self.test_file, 'r') as file:
            data = json.load(file)
        
        self.assertEqual(data[0]["status"], "in progress")

    @patch('builtins.print')
    def test_list_tasks(self, mock_print):
        """Test listing tasks with different status filters."""
        # Create multiple tasks with different statuses
        task1 = Task("Task 1", "todo", self.test_file)
        task2 = Task("Task 2", "in progress", self.test_file)
        task1.add_task()
        task2.add_task()
        
        # Test listing all tasks
        Task.list_tasks(file_name=self.test_file)
        mock_print.assert_any_call("Task 1")
        mock_print.assert_any_call("Task 2")
        
        # Reset mock
        mock_print.reset_mock()
        
        # Test listing only in-progress tasks
        Task.list_tasks(status="in-progress", file_name=self.test_file)
        mock_print.assert_called_once_with("Task 2")

    def test_input_parse_command(self):
        """Test command parsing from input."""
        from task_tracker import input_parse_command
        
        # Test basic command
        result = input_parse_command("add task")
        self.assertEqual(result, ["add", "task"])
        
        # Test single word command
        result = input_parse_command("help")
        self.assertEqual(result, ["help"])

    def test_input_parse_description(self):
        """Test description parsing from input."""
        from task_tracker import input_parse_description
        
        # Test quoted description
        result = input_parse_description('add "This is a task"')
        self.assertEqual(result, "This is a task")
        
        # Test unquoted description
        result = input_parse_description("Simple task")
        self.assertEqual(result, "Simple task")

    @patch('builtins.print')
    def test_error_handling(self, mock_print):
        """Test error handling for various scenarios."""
        # Test updating non-existent task
        Task.update_task("non-existent-id", "Updated task", self.test_file)
        
        # Add assertions to verify error messages
        mock_print.assert_any_call("task not found")

    def test_invalid_task_creation(self):
        """Test that task creation fails with invalid input."""
        # Test empty description
        with self.assertRaises(ValueError):
            Task("", "todo", self.test_file)
        
        # Test invalid status
        with self.assertRaises(ValueError):
            Task("Test task", "invalid_status", self.test_file)

    def test_duplicate_task_handling(self):
        """Test handling of duplicate tasks."""
        task1 = Task("Test task", "todo", self.test_file)
        task1.add_task()
        
        # Add same task again
        task2 = Task("Test task", "todo", self.test_file)
        task2.add_task()
        
        # Verify both tasks exist but have different IDs
        with open(self.test_file, 'r') as file:
            data = json.load(file)
        
        self.assertEqual(len(data), 2)
        self.assertNotEqual(data[0]["id"], data[1]["id"])

    @patch('builtins.print')
    def test_list_tasks_empty_file(self, mock_print):
        """Test listing tasks with an empty file."""
        Task.list_tasks(file_name=self.test_file)
        mock_print.assert_called_once_with("No tasks found")

    def test_task_status_transitions(self):
        """Test all possible task status transitions."""
        task = Task("Test task", "todo", self.test_file)
        task.add_task()
        task_id = str(task.id)
        
        # todo -> in progress
        Task.mark_in_progress(task_id, self.test_file)
        with open(self.test_file, 'r') as file:
            data = json.load(file)
        self.assertEqual(data[0]["status"], "in progress")
        
        # in progress -> done
        Task.mark_done(task_id, self.test_file)
        with open(self.test_file, 'r') as file:
            data = json.load(file)
        self.assertEqual(data[0]["status"], "done")

    def test_task_operations(self):
        """Test all CRUD operations in sequence."""
        with self.subTest("Create and Add"):
            task = Task("Test task", "todo", self.test_file)
            task.add_task()
            self.assertIsNotNone(task.id)

        with self.subTest("Read"):
            with open(self.test_file, 'r') as file:
                data = json.load(file)
            self.assertEqual(len(data), 1)

        with self.subTest("Update"):
            Task.update_task(str(task.id), "Updated task", self.test_file)
            with open(self.test_file, 'r') as file:
                data = json.load(file)
            self.assertEqual(data[0]["description"], "Updated task")

        with self.subTest("Delete"):
            Task.delete_task(str(task.id), self.test_file)
            with open(self.test_file, 'r') as file:
                data = json.load(file)
            self.assertEqual(len(data), 0)

    def test_performance_large_dataset(self):
        """Test performance with a large number of tasks."""
        # Create 100 tasks
        tasks = []
        for i in range(100):
            task = Task(f"Task {i}", "todo", self.test_file)
            task.add_task()
            tasks.append(task)
        
        # Time listing operation
        import time
        start_time = time.time()
        Task.list_tasks(file_name=self.test_file)
        end_time = time.time()
        
        # Assert operation completed in reasonable time (e.g., under 1 second)
        self.assertLess(end_time - start_time, 1.0)

if __name__ == '__main__':
    unittest.main()