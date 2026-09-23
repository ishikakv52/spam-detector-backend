from django.db.models import Count, Q
from .models import Message
from .constants import Classification


def get_user_messages(user):
    return Message.objects.filter(user=user)


def get_dashboard_stats(user):
    qs = get_user_messages(user)
    total = qs.count()
    spam_count = qs.filter(classification=Classification.SPAM).count()
    not_spam_count = qs.filter(classification=Classification.NOT_SPAM).count()
    spam_percentage = round((spam_count / total) * 100, 1) if total else 0.0

    return {
        "total_messages": total,
        "spam_count": spam_count,
        "not_spam_count": not_spam_count,
        "spam_percentage": spam_percentage,
        "recent_messages": qs.order_by("-created_at")[:5],
    }
