from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Message
from .selectors import get_user_messages, get_dashboard_stats
from .services import analyze_message, GeminiAnalysisError
from .serializers import (
    MessageSerializer,
    MessageUpdateSerializer,
    AnalyzeRequestSerializer,
    DashboardSerializer,
)


class MessageViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for a user's own messages, plus a POST /messages/analyze/ action
    that calls Gemini and saves the result in one step.
    A user can only ever see or touch their own records.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_user_messages(self.request.user)

    def get_serializer_class(self):
        if self.action in ("update", "partial_update"):
            return MessageUpdateSerializer
        return MessageSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["post"])
    def analyze(self, request):
        """
        Body: {"message_text": "..."}
        Sends the text to Gemini, saves the result under the current user,
        and returns the saved record.
        """
        req_serializer = AnalyzeRequestSerializer(data=request.data)
        req_serializer.is_valid(raise_exception=True)
        message_text = req_serializer.validated_data["message_text"]

        try:
            result = analyze_message(message_text)
        except GeminiAnalysisError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        record = Message.objects.create(
            user=request.user,
            message_text=message_text,
            **result,
        )
        return Response(MessageSerializer(record).data, status=status.HTTP_201_CREATED)


class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stats = get_dashboard_stats(request.user)
        return Response(DashboardSerializer(stats).data)
