from django.urls import path, include
from .views import create_user, registration_view

urlpatterns = [
    path('create_user/', create_user, name='create_user'),
    path('register_user/', registration_view, name='register_user')
]