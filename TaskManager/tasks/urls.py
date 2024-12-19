from django.urls import path, include
from .views import TaskViewSet, create_user
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('create_user/', create_user, name='create_user')
]