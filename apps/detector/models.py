from django.conf import settings
from django.db import models
from .constants import Classification, Category


class Message(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages"
    )
    message_text = models.TextField()

    classification = models.CharField(
        max_length=20, choices=Classification.CHOICES, blank=True
    )
    category = models.CharField(max_length=30, choices=Category.CHOICES, blank=True)
    explanation = models.TextField(blank=True)
    suspicious_indicators = models.JSONField(default=list, blank=True)
    safety_suggestion = models.TextField(blank=True)

    user_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}: {self.message_text[:40]}"
