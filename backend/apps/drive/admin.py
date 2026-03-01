from django.contrib import admin

from .models import Node


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "owner", "parent", "is_shared", "created_at")
    list_filter = ("type", "is_shared", "created_at")
    search_fields = ("name", "owner__email")
