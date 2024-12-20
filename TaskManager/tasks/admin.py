from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Task
from users.models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # List display for the user listing page
    list_display = ['username', 'email', 'role', 'is_active', 'is_staff']
    
    # Add filter options
    list_filter = ['role', 'is_active', 'is_staff']

    # Search fields to make searching easier in the admin panel
    search_fields = ['username', 'email']
    
    # Ordering of how the users appear in the list
    ordering = ['username']

    # Fields to display and edit when viewing or editing the user
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),  # Add role to the user view
    )
    
    # Fields to display when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),  # Add role to the user creation form
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Task)