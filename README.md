
# **Task Management Application**

## **Overview**
This is a Django-based Task Management Application that allows users to create, update, and manage tasks. The application supports user roles, including **admin** and **regular users**, with role-based access control to tasks and features. Admin users can manage tasks for all users, while regular users can only manage their own tasks.

---

## **Features**
- **Role-Based Access Control**:
  - Admins can manage tasks for any user.
  - Regular users can only manage their own tasks.
- **JWT-Based Authentication**:
  - Secure user authentication and token management.
- **Soft Deletion**:
  - Tasks are marked as inactive instead of being deleted.
- **Task Filters**:
  - Filter tasks by status or due date.
- **Pagination**:
  - Paginated responses for large datasets.

---

## **Prerequisites**
- Python 3.8+
- Django 4.x
- PostgreSQL or SQLite for the database
- pip (Python package installer)

---

## **Setup Instructions**

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

### Step 4: Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create a Superuser
```bash
python manage.py createsuperuser
```

### Step 6: Run the Development Server
```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000/`.

---

## **Project Structure**

```
TaskManager/
├── tasks/                # Task management app
│   ├── admin.py          # Admin configurations for tasks
│   ├── apps.py           # Task app configurations
│   ├── migrations/       # Database migrations
│   ├── models.py         # Task model
|   ├── permissions.py    # Custom permissions
│   ├── serializers.py    # Task serializers
│   ├── tests.py          # Task tests
│   ├── urls.py           # Task URLs
│   └── views.py          # Task API views
│
├── users/                # User management app
│   ├── admin.py          # Admin configurations for users
│   ├── apps.py           # User app configurations
│   ├── migrations/       # Database migrations
│   ├── models.py         # CustomUser model
│   ├── serializers.py    # User serializers
│   ├── tests.py          # User tests
│   ├── urls.py           # User URLs
│   └── views.py          # User API views
│
├── TaskManager/          # Project-level configurations
│   ├── settings.py       # Django settings
│   ├── urls.py           # Project URL configurations
│
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── .gitignore            # Git ignore file
```

---

## **API Endpoints**

### **Authentication**
| Method | Endpoint               | Description                     |
|--------|-------------------------|---------------------------------|
| POST   | `/api/token/`           | Obtain JWT token               |
| POST   | `/api/token/refresh/`   | Refresh JWT token              |
| POST   | `/api/users/register_user/`   | Register a new user            |
| POST   | `/api/users/create_user/`     | Create a user (admin only)     |

---

### **Tasks**
| Method | Endpoint                | Description                        |
|--------|--------------------------|------------------------------------|
| GET    | `/api/tasks/`            | List all tasks (admin) / own tasks |
| POST   | `/api/tasks/`            | Create a new task                  |
| GET    | `/api/tasks/{id}/`       | Retrieve a specific task           |
| PUT    | `/api/tasks/{id}/`       | Update a specific task             |
| DELETE | `/api/tasks/{id}/`       | Soft delete a specific task        |

---

### **Filters**
| Parameter  | Description                       |
|------------|-----------------------------------|
| `status`   | Filter tasks by status           |
| `due_date` | Filter tasks by due date         |

Example:
```bash
GET /api/tasks/?status=pending&due_date=2024-12-31
```

---

### **Pagination**
| Parameter    | Description                        |
|--------------|------------------------------------|
| `page`       | Specify the page number           |
| `page_size`  | Specify the number of items per page |

Example:
```bash
GET /api/tasks/?page=1&page_size=20
```

---

## **Running Tests**

Run the test suite to ensure the application works as expected:
```bash
python manage.py test tasks
python manage.py test users
```

---

## **Key Features**
- **Soft Deletion:** Tasks are marked as inactive instead of being permanently removed.
- **Role-Based Access Control:** Admins can manage all tasks; regular users can only manage their own tasks.
- **Filters and Pagination:** Easily navigate and filter through large datasets.

---

## **Contributing**
Feel free to open issues or submit pull requests for any enhancements or bug fixes.

--- 
