from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser

User = get_user_model()

class UserViewSetTests(APITestCase):
    
    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_user(
            username="admin", email="admin@example.com", password="adminpass", role="admin"
        )

        # Create regular user
        self.regular_user = User.objects.create_user(
            username="user", email="user@example.com", password="userpass", role="regular"
        )

        
        self.user_data = {
            "username": "new_user",
            "email": "new_user@example.com",
            "password": "newuserpass",
            "role": "regular",
        }
        self.valid_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newuserpass",
        }
        self.invalid_data = {
            "username": "",
            "email": "invalidemail",  # Invalid email format
            "password": "short",  # Password too short
        }
        # Generate JWT token for authentication
        self.regular_user_token = str(RefreshToken.for_user(self.regular_user).access_token)
        self.admin_user_token = str(RefreshToken.for_user(self.admin_user).access_token)


    def test_create_user_as_admin(self):
        """Test that an admin can create a new user."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_user_token}")
        response = self.client.post("/api/users/create_user/", self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["detail"], "User created successfully.")
        self.assertEqual(response.data["user"]["username"], self.user_data["username"])

    def test_create_user_as_regular_user(self):
        """Test that a regular user cannot create a new user."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.regular_user_token}")
        response = self.client.post("/api/users/create_user/", self.user_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "You are not authorized to create users.")

    def test_create_user_invalid_data(self):
        """Test creating a user with invalid data."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_user_token}")
        invalid_data = {
            "username": "",  # Missing username
            "email": "invalid-email",  # Invalid email
            "password": "short",  # Short password
        }
        response = self.client.post("/api/users/create_user/", invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)


    def test_registration_success(self):
        url = '/api/users/register_user/'
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword123",
            "password_confirmation": "securepassword123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)

    def test_registration_password_mismatch(self):
        url = '/api/users/register_user/'
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword123",
            "password_confirmation": "differentpassword"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_registration_duplicate_email(self):
        CustomUser.objects.create_user(username="existinguser", email="existing@example.com", password="password123")
        url = '/api/users/register_user/'
        data = {
            "username": "newuser",
            "email": "existing@example.com",
            "password": "securepassword123",
            "password_confirmation": "securepassword123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

