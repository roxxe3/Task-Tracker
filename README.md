# Task Management CLI

## Overview

This is a command-line interface (CLI) application for managing tasks. The application allows you to create, update, delete, and list tasks with various statuses.

## Features

- Add new tasks
- Update existing tasks
- Mark tasks as in progress
- Delete tasks
- List tasks (with optional filtering by status)
- Simple and intuitive command-line interface

## Requirements

- Python 3.10+
- Standard Python libraries (json, uuid, datetime)

## Installation

1. Clone the repository
2. Ensure you have Python 3.10 or higher installed
3. No additional dependencies required

## Usage

### Available Commands

- `add "Task description"`: Add a new task
- `update <task-id> "New task description"`: Update an existing task
- `mark-in-progress <task-id>`: Mark a task as in progress
- `mark-done <task-id>`: Mark a task as completed
- `delete <task-id>`: Delete a specific task
- `list`: List all tasks
- `list in-progress`: List tasks with 'in progress' status
- `help`: Show available commands
- `exit`: Exit the application

### Examples

```bash
# Add a new task
task-cli > add "Write project documentation"

# Update an existing task
task-cli > update 123e4567-e89b-12d3-a456-426614174000 "Update project documentation"

# Mark a task as in progress
task-cli > mark-in-progress 123e4567-e89b-12d3-a456-426614174000

# Delete a task
task-cli > delete 123e4567-e89b-12d3-a456-426614174000

# List all tasks
task-cli > list

# List in-progress tasks
task-cli > list in-progress
```

## Data Storage

Tasks are stored in a `data.json` file in the following format:

```json
[
    {
        "id": "unique-uuid",
        "description": "Task description",
        "status": "in progress",
        "createdAt": "timestamp",
        "updatedAt": "timestamp"
    }
]
```

## Error Handling

- The application handles file reading/writing errors gracefully
- Provides clear error messages for invalid commands
- Supports keyboard interrupt (Ctrl+C) for safe exit

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request


## Author

Hamza Fariss

