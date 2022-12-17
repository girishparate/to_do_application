from schedule_task.models import Notification
from .models import Label

def main_dashboard_context(request):
    data = {}
    if request.user.is_authenticated:
        data = {'unread_notification': Notification.objects.filter(user=request.user, read=False).count(), 'label': Label.objects.filter(user=request.user)}
    return data