# 🧠 Task Tracker CLI

A production-ready **Command Line Task Manager** built with pure Python.
This project demonstrates clean architecture, OOP principles, JSON
persistence, and CLI argument parsing.

------------------------------------------------------------------------

## 🚀 Features

-   Add tasks
-   Update task description
-   Delete tasks
-   Change task status (`todo`, `in-progress`, `done`)
-   List all tasks
-   Filter tasks by status
-   Persistent storage using JSON
-   Automatic timestamps
-   Clean OOP architecture

------------------------------------------------------------------------

## 🏗 Project Structure

    task_tracker.py
    tasks_database.json (auto-generated)

------------------------------------------------------------------------

## ⚙️ Installation

``` bash
git clone https://github.com/your-username/task-tracker-cli.git
cd task-tracker-cli
```

Python version required:

    Python 3.10+

------------------------------------------------------------------------

## 📖 Usage

    python task_tracker.py <command> [arguments]

------------------------------------------------------------------------

## 🛠 Available Commands

### Add Task

    python task_tracker.py add "Buy groceries"

### Update Task

    python task_tracker.py update 1 "Buy groceries and milk"

### Delete Task

    python task_tracker.py delete 1

### Change Status

Mark as in progress:

    python task_tracker.py mark-in-progress 1

Mark as done:

    python task_tracker.py mark-done 1

### List Tasks

Show all:

    python task_tracker.py list

Filter:

    python task_tracker.py list done
    python task_tracker.py list in-progress
    python task_tracker.py list todo

------------------------------------------------------------------------

## 💾 Data Storage

Tasks are stored in:

    tasks_database.json

Example:

``` json
[
  {
    "id": 1,
    "description": "Buy groceries",
    "status": "todo",
    "created_at": "Mon Feb 24 12:00:00 2026",
    "update_at": "Mon Feb 24 12:00:00 2026"
  }
]
```

------------------------------------------------------------------------

## 🧠 Technical Highlights

-   Object-Oriented Design
-   Class-level ID counter recovery
-   Static & Class methods
-   Match-case routing (Python 3.10+)
-   Graceful error handling
-   Type hints
-   UTF-8 JSON support

------------------------------------------------------------------------

## 🔮 Future Improvements

-   argparse integration
-   Unit tests (pytest)
-   Logging system
-   Docker support
-   REST API version (FastAPI)
-   SQLite backend
-   Task priorities & deadlines

------------------------------------------------------------------------

## 👨‍💻 Author

Your Name\
Python Backend Developer

------------------------------------------------------------------------

## 📄 License

MIT License
