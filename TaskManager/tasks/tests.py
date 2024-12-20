from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Task
from datetime import date

User = get_user_model()

class TaskViewSetTests(APITestCase):
    
    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_user(
            username="admin", email="admin@example.com", password="adminpass", role="admin"
        )

        # Create regular user
        self.regular_user = User.objects.create_user(
            username="user", email="user@example.com", password="userpass", role="regular"
        )

        # Create tasks
        self.task1 = Task.objects.create(
            task_name="Task 1", description="Task 1 description", due_date=date(2024, 12, 25), user=self.regular_user, is_active=True
        )
        self.task2 = Task.objects.create(
            task_name="Task 2", description="Task 2 description", due_date=date(2024, 12, 26), user=self.regular_user, is_active=True
        )
        self.task3 = Task.objects.create(
            task_name="Task 3", description="Task 3 description", due_date=date(2024, 12, 27), user=self.admin_user, is_active=True
        )
        
        # Generate JWT token for authentication
        self.regular_user_token = str(RefreshToken.for_user(self.regular_user).access_token)
        self.admin_user_token = str(RefreshToken.for_user(self.admin_user).access_token)

    # Test Case 1: Admin can create a task for any user
    def test_create_task_admin(self):
        url = '/api/tasks/'
        data = {
            'task_name': 'Admin Task',
            'description': 'Admin created task',
            'due_date': '2024-12-31',
            'user': self.regular_user.id
        }
        print(self.admin_user)
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_user_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['detail'], "Task created successfully.")

    # Test Case 2: Regular user can only create their own task
    def test_create_task_regular_user(self):
        url = '/api/tasks/'
        data = {
            'task_name': 'User Task',
            'description': 'User created task',
            'due_date': '2024-12-31'
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {self.regular_user_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test Case 3: Regular user cannot create task for another user
    def test_create_task_regular_user_other_user(self):
        url = '/api/tasks/'
        data = {
            'task_name': 'Other User Task',
            'description': 'User cannot create task for another',
            'due_date': '2024-12-31',
            'user': self.admin_user.id
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {self.regular_user_token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "You are not authorized to create tasks for another user.")

    # Test Case 4: Admin can view any task
    def test_retrieve_task_admin(self):
        url = f'/api/tasks/{self.task1.id}/'  # Ensure leading slash
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.admin_user_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], "Task retrieved successfully.")


    # Test Case 5: Regular user can only view their own tasks
    def test_retrieve_task_regular_user(self):
        url = f'/api/tasks/{self.task1.id}/'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.regular_user_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], "Task retrieved successfully.")
    
    def test_retrieve_task_other_user(self):
        url = f'/api/tasks/{self.task3.id}/'  # Task assigned to a different user
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.regular_user_token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "You are not authorized to view this task.")


    # Test Case 6: Regular user cannot update another user's task
    def test_update_task_regular_user(self):
        url = f'/api/tasks/{self.task1.id}/'
        data = {'task_name': 'Updated Task 1'}
        response = self.client.patch(url, data, HTTP_AUTHORIZATION=f'Bearer {self.regular_user_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # Test Case 7: Admin can reassign tasks (change user)
    def test_update_task_admin_reassign(self):
        url = f'/api/tasks/{self.task1.id}/'
        data = {'user': self.admin_user.id}  # Reassign task to admin
        response = self.client.patch(url, data, HTTP_AUTHORIZATION=f'Bearer {self.admin_user_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test Case 8: Task soft delete (admin and user permissions)
    def test_delete_task_admin(self):
        url = f'/api/tasks/{self.task1.id}/'
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {self.admin_user_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_task_regular_user(self):
        url = f'/api/tasks/{self.task1.id}/'
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Bearer {self.regular_user_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test Case 9: Filter tasks by status
    def test_filter_task_status(self):
        url = '/api/tasks/?status=pending'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.regular_user_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)

    # Test Case 10: Pagination Test
    def test_task_pagination(self):
        url = '/api/tasks/?page=1'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.regular_user_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data)
        self.assertTrue(len(response.data['results']) <= 5)  # Assuming page size is 5