from .models import Notification
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer


class NotificationPage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'notification.html'

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        data = {'notificationn_list': notifications}
        return Response(data)

class NotificationRead(APIView):
    def get(self, request, pk):
        notification = Notification.objects.get(pk=pk)
        notification.read=True
        notification.save()
        return redirect('/task-details/'+notification.to_do.slug)