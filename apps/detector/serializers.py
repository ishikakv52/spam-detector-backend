from rest_framework import serializers
from .models import Message
from .validators import validate_message_text


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            "id",
            "message_text",
            "classification",
            "category",
            "explanation",
            "suspicious_indicators",
            "safety_suggestion",
            "user_notes",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "classification",
            "category",
            "explanation",
            "suspicious_indicators",
            "safety_suggestion",
            "created_at",
            "updated_at",
        )

    def validate_message_text(self, value):
        return validate_message_text(value)


class MessageUpdateSerializer(serializers.ModelSerializer):
    """Users may only edit their own notes on a saved record."""
    class Meta:
        model = Message
        fields = ("user_notes",)


class AnalyzeRequestSerializer(serializers.Serializer):
    message_text = serializers.CharField()

    def validate_message_text(self, value):
        return validate_message_text(value)


class DashboardSerializer(serializers.Serializer):
    total_messages = serializers.IntegerField()
    spam_count = serializers.IntegerField()
    not_spam_count = serializers.IntegerField()
    spam_percentage = serializers.FloatField()
    recent_messages = MessageSerializer(many=True)
