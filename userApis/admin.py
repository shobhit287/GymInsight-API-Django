from django.contrib import admin
from .models import User  # Import your models

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'email', 'created_at', 'first_name', 'last_name', 'password', 'updated_at')
    search_fields = ('email','user_id')
    ordering = ('-created_at',)
