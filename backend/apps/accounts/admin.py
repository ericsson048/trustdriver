from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_staff", "is_active", "created_at")
    search_fields = ("email",)
    ordering = ("email",)
