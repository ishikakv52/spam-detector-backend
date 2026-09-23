from rest_framework import serializers
from .constants import MAX_MESSAGE_LENGTH


def validate_message_text(value: str) -> str:
    text = (value or "").strip()
    if not text:
        raise serializers.ValidationError("Message text cannot be empty.")
    if len(text) > MAX_MESSAGE_LENGTH:
        raise serializers.ValidationError(
            f"Message text cannot exceed {MAX_MESSAGE_LENGTH} characters."
        )
    return text
