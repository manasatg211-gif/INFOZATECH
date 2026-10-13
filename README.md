# TaskFlow — Smart To-Do Manager

A Flask + SQLite task management web application built for the InfozaTech Python Development Internship, Task 1.

## Features

- Add tasks with a title, description, priority, and optional due date
- View all tasks and pending/completed status
- Mark tasks complete or pending
- Delete a task or clear all completed tasks
- Search task titles and descriptions
- Filter by status and priority
- Sort tasks by completion, priority, and due date
- Store tasks persistently in SQLite
- Responsive layout for desktop and mobile
- Input validation and parameterized SQL queries

## Requirements

- Python 3.10 or newer
- pip
- A modern browser

## Run locally

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

SQLite is included with Python, so no separate database installation is needed. The `tasks.db` file is created automatically the first time the app starts.

## Project structure

```text
TaskFlow_InfozaTech/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## Manual test checklist

1. Add a task with a title, description, priority, and due date.
2. Try submitting an empty title; the app should reject it.
3. Mark a task complete, then mark it pending again.
4. Search for a word in a task title or description.
5. Filter by pending/completed status and priority.
6. Delete one task after confirming the prompt.
7. Restart the Flask app and confirm remaining tasks are still saved.
8. Clear completed tasks and confirm pending tasks remain.

## Notes

- This is a local learning/demo application. Do not deploy the development server publicly as-is.
- Before public deployment, set a strong secret key using an environment variable, add CSRF protection, and use a production WSGI server.
- Bootstrap and Google Fonts are loaded from CDNs, so those visual assets require an internet connection. The core Flask application and SQLite storage run locally.

## Internship submission

Create a separate GitHub repository named `INFOZATECH`, add this project, test it, and include a short demo video link in your LinkedIn post. Explain the code in your own words and follow the internship provider's submission instructions.
