from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, DashboardView

router = DefaultRouter()
router.register("messages", MessageViewSet, basename="message")

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("", include(router.urls)),
]
