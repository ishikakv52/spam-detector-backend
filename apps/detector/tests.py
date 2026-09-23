from unittest.mock import patch
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Message

FAKE_ANALYSIS = {
    "classification": "spam",
    "category": "prize_reward",
    "explanation": "Unexpected prize claim with urgency.",
    "suspicious_indicators": ["prize claim", "urgent language"],
    "safety_suggestion": "Do not click the link.",
}


class AuthFlowTests(APITestCase):
    def test_register_and_login(self):
        register_url = reverse("register")
        resp = self.client.post(register_url, {
            "username": "jaat",
            "email": "jaat@example.com",
            "password": "StrongPass123",
            "password_confirm": "StrongPass123",
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        login_url = reverse("login")
        resp = self.client.post(login_url, {"username": "jaat", "password": "StrongPass123"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("access", resp.data)
        self.assertIn("refresh", resp.data)


class MessageApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="jaat", password="StrongPass123")
        self.other_user = User.objects.create_user(username="other", password="StrongPass123")
        self.client.force_authenticate(user=self.user)

    @patch("apps.detector.views.analyze_message", return_value=FAKE_ANALYSIS)
    def test_analyze_creates_message_for_current_user(self, mock_analyze):
        resp = self.client.post("/api/messages/analyze/", {
            "message_text": "You won a prize, click here!"
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["classification"], "spam")
        self.assertEqual(Message.objects.filter(user=self.user).count(), 1)

    def test_user_cannot_see_other_users_messages(self):
        Message.objects.create(
            user=self.other_user,
            message_text="private to other user",
            classification="not_spam",
        )
        resp = self.client.get("/api/messages/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        ids = [m["id"] for m in resp.data["results"]] if "results" in resp.data else [m["id"] for m in resp.data]
        self.assertEqual(len(ids), 0)

    def test_dashboard_stats(self):
        Message.objects.create(user=self.user, message_text="a", classification="spam")
        Message.objects.create(user=self.user, message_text="b", classification="not_spam")
        resp = self.client.get(reverse("dashboard"))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["total_messages"], 2)
        self.assertEqual(resp.data["spam_count"], 1)
        self.assertEqual(resp.data["not_spam_count"], 1)
