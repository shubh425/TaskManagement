# Task Management Application

## Overview
This is a Django-based Task Management Application that allows users to create, update, and manage tasks. The application supports user roles, including **admin** and **regular users**, with role-based access control to tasks and their features. Admin users can manage tasks for all users, while regular users can only manage their own tasks.

---

## Features
- Role-based access control (Admin vs Regular Users).
- Task creation, update, retrieval, deletion (soft delete).
- Filters for task status and due dates.
- Pagination for large datasets.
- JWT-based authentication.

---

## Prerequisites
- Python 3.8+
- Django 4.x
- PostgreSQL or SQLite for database
- pip (Python package installer)

---

## Setup Instructions

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd TaskManager
```

### Step 2: Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the root directory and include the following variables:
```env
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3  # Use PostgreSQL if preferred
```

### Step 5: Apply Migrations
```bash
python manage.py makemigrations\python manage.py migrate
```

### Step 6: Create a Superuser
```bash
python manage.py createsuperuser
```

### Step 7: Run the Development Server
```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000/`.

---

## Running Tests

Run the test suite to ensure the application works as expected:
```bash
python manage.py test tasks
```

---

## Project Structure
```
TaskManager/
├── tasks/                # Core app for managing tasks
│   ├── admin.py          # Admin panel configurations
│   ├── apps.py           # App configurations
│   ├── migrations/       # Database migrations
│   ├── models.py         # Task and CustomUser models
│   ├── permissions.py    # Custom permissions
│   ├── serializers.py    # DRF serializers
│   ├── tests.py          # Unit tests
│   ├── urls.py           # Task app URLs
│   └── views.py          # API views
│
├── TaskManager/          # Project settings and configurations
│   ├── settings.py       # Django settings
│   ├── urls.py           # Project URL configuration
│
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── .gitignore            # Git ignore file
```

---

## API Endpoints

### Authentication
| Method | Endpoint            | Description                  |
|--------|---------------------|------------------------------|
| POST   | `/api/token/`       | Obtain JWT token             |
| POST   | `/api/token/refresh/` | Refresh JWT token           |

### Tasks
| Method | Endpoint               | Description                       |
|--------|-------------------------|-----------------------------------|
| GET    | `/api/tasks/`          | List all tasks (admin) / own tasks |
| POST   | `/api/tasks/`          | Create a task                    |
| GET    | `/api/tasks/{id}/`     | Retrieve a specific task         |
| PUT    | `/api/tasks/{id}/`     | Update a task                    |
| DELETE | `/api/tasks/{id}/`     | Soft delete a task               |

### Filters
Use query parameters to filter tasks:
- `status`: Filter by task status (e.g., pending, completed).
- `due_date`: Filter by due date.

Example:
```bash
GET /api/tasks/?status=pending&due_date=2024-12-31
```

### Pagination
By default, API responses are paginated with a page size of 5. You can use the page query parameter to navigate through pages, like so:

Example:
```bash
GET /api/tasks/?page=2
```

You can adjust the page_size parameter if you wish to change the number of items per page.

Example:
```bash
GET /api/tasks/?page=1&page_size=20
```
---

## Additional Notes
- **Soft Deletion:** Tasks are marked as inactive instead of being removed from the database.
- **Role-Based Access Control:** Admins can manage all tasks; regular users are restricted to their own tasks.
- **Pagination:** Responses are paginated with a default page size of 10.

---

## Contributing
Feel free to open issues or submit pull requests for any enhancements or bug fixes.

---
