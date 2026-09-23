from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "classification", "category", "created_at")
    list_filter = ("classification", "category")
    search_fields = ("message_text", "user__username")
