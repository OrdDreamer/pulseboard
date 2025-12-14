# 🧩 Pulseboard - Task Manager for IT Company

## 📘 Project Description

**Pulseboard** is an educational web application for task management in an IT company. The system allows teams of developers, designers, project managers, and QA specialists to efficiently manage tasks, assign them to team members, and track progress.

Each team member can:
- create tasks
- assign tasks to other team members
- mark tasks as completed
- view task completion statistics

---

## ✨ Features

### Task Management
- **CRUD operations**: create, view, edit, and delete tasks
- **Assignee assignment**: ability to assign tasks to one or multiple workers
- **Priorities**: set task priority (Urgent, High, Medium, Low)
- **Task types**: task classification (Bug, New feature, Breaking change, Refactoring, QA)
- **Deadlines**: set and track completion deadlines
- **Completion status**: mark tasks as completed
- **Search**: search tasks by name or description
- **Filtering**: filter tasks by status (completed/incomplete), priority, task type, deadline (today, next 3 days, next week, overdue) and assignee

### Worker Management
- **Worker list**: view all team members with their positions
- **Worker profile**: detailed information about a worker and their tasks
- **Profile editing**: ability to update your own profile
- **Search**: search workers by first name, last name, or username
- **Filtering**: filter workers by position

### Statistics Dashboard
- **Personal statistics**: 
  - total number of tasks
  - completed and incomplete tasks
  - overdue tasks
  - completion percentage
  - distribution by priorities and types
- **Team statistics**: similar statistics for the entire team
- **Top 5 workers**: workers with the most tasks

### Authentication and Registration
- **Registration**: create a new account
- **Login**: user authentication
- **Logout**: secure logout from the system
- **Route protection**: access to functionality only for authorized users

---

## 🛠️ Technologies

- **Python 3.8+**
- **Django 5.2.8**
- **SQLite**
- **Bootstrap 5**
- **Django Crispy Forms**
- **Chart.js 4.4.0**

---

## 📋 Installation

### Requirements

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the repository

```bash
git clone https://github.com/OrdDreamer/pulseboard
cd pulseboard
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment:

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Apply migrations

```bash
python manage.py migrate
```

### Step 5: Load fixtures

To load test data (positions, task types, workers, tasks):

```bash
python manage.py loaddata core/fixtures/initial_data.json
```

---

## 🚀 Running the Project

After completing all installation steps, start the development server:

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

---

## 👤 Test Credentials

After loading the fixtures, you can log in to the system using the following credentials:

- **Username:** `admin`
- **Password:** `admin`

This account has superuser privileges and allows:
- full access to all application features
- access to Django admin panel (http://127.0.0.1:8000/admin/)
- create, edit, and delete tasks
- view and edit worker profiles
- view team statistics

---

## 📁 Project Structure

```
pulseboard/
├── core/                      # Main Django app
│   ├── fixtures/              # Fixtures with test data
│   │   └── initial_data.json
│   ├── migrations/            # Database migrations
│   ├── models.py              # Data models
│   ├── views.py               # Views
│   ├── forms.py               # Forms
│   ├── urls.py                # URL routes
│   └── admin.py               # Admin panel settings
├── pulseboard/                # Project settings
│   ├── settings.py            # Django settings
│   └── urls.py                # Main URL routes
├── templates/                 # HTML templates
│   ├── base.html              # Base template
│   ├── base_auth.html         # Base template for authentication
│   └── core/                  # Templates for core app
│       ├── index.html         # Statistics dashboard
│       ├── task_list.html     # Task list
│       ├── task_detail.html   # Task details
│       ├── task_form.html     # Task create/edit form
│       ├── task_confirm_delete.html # Task deletion confirmation
│       ├── worker_list.html   # Worker list
│       ├── worker_detail.html # Worker profile
│       └── worker_form.html   # Worker edit form
├── static/                    # Static files (CSS, images)
│   ├── css/
│   └── images/
├── db.sqlite3               # SQLite database
├── manage.py                # Django management script
├── requirements.txt         # Project dependencies
└── README.md                # Documentation
```

---

## 🗄️ Data Models

### Position
- `name` — position name (Developer, Project Manager, QA, Designer, DevOps)
- Relationship: Position → Worker (1 → n)

### Worker
Extends Django AbstractUser:
- `position` — worker's position (ForeignKey to Position)
- `username`, `email`, `password` — standard user fields
- `first_name`, `last_name` — first and last name
- Relationships: 
  - Position → Worker (1 → n)
  - Worker ↔ Task (ManyToMany)

### TaskType
- `name` — type name (Bug, New feature, Breaking change, Refactoring, QA)
- Relationship: TaskType → Task (1 → n)

### Task
- `name` — task name
- `description` — task description
- `deadline` — completion deadline
- `is_completed` — completion status (True/False)
- `priority` — priority (Urgent, High, Medium, Low)
- `task_type` — task type (ForeignKey to TaskType)
- `assignees` — assignees (ManyToMany to Worker)
- Relationships:
  - TaskType → Task (1 → n)
  - Task ↔ Worker (ManyToMany)

---

## 🔗 Main URL Routes

- `/` — home page (dashboard)
- `/tasks/` — task list
- `/tasks/create/` — create new task
- `/tasks/<id>/` — task details
- `/tasks/<id>/update/` — edit task
- `/tasks/<id>/delete/` — delete task
- `/workers/` — worker list
- `/workers/<id>/` — worker profile
- `/workers/<id>/update/` — edit profile
- `/login/` — login
- `/logout/` — logout
- `/register/` — register new user
- `/admin/` — Django admin panel

---

## 📝 Additional Notes

- The project uses a custom user model `Worker` that extends `AbstractUser`
- All views are protected via `LoginRequiredMixin`
- Pagination is used for task and worker lists (20 items per page)
- The dashboard contains statistics visualization using charts
- Forms are styled using Bootstrap 5 via Django Crispy Forms

---

## 📄 License

This is an educational project created for educational purposes.
