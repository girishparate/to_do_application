from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import *
from .serializers import *
from schedule_task.tasks import schedule_todo
from datetime import datetime, timezone
from django.utils.text import slugify


# Create your views here.
class MainDashboard(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main_dashboard.html'

    def get(self, request):
        """
        get method which will return the task raised by the current user on main dashboard ( home screen )
        """
        data = {"title": "To Do Application",
                "tasks": ToDo.objects.filter(user=request.user)
                }
        return Response(data)

    def post(self, request):
        """
        post method to save new task raised by the user, with multiple label selection and image data as file input
        """
        serializer = ToDoSerializer(data=request.data)
        label = request.POST.getlist('label')
        image = request.FILES.get('image')
        if serializer.is_valid():

            serializer_saved = serializer.save(user=request.user, image=image)
            serializer_saved.slug = slugify(serializer_saved.title)
            serializer_saved.save()
            if serializer_saved.reminds_on != None:
                serializer_saved.reminder = True
                serializer_saved.save()
                countdown = (serializer_saved.reminds_on - datetime.now(timezone.utc)).total_seconds()
                task = schedule_todo.apply_async(args=[serializer_saved.id, request.user.id], countdown=countdown)
                serializer_saved.task_id = task
                serializer_saved.save()
            task = ToDo.objects.get(id=serializer_saved.pk)
            task.label.add(*label)

            messages.success(request, "New task added successfully!!!")
        else:
            messages.error(request, "Cannot create new task")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class ToDoCrudOperation(APIView):
    def get(self, request, slug):
        to_do = ToDo.objects.get(slug=slug)
        data = {'to_do': to_do, "title": to_do.title}

        return render(request, 'task_detail.html', data)

    def put(self, request, pk):
        """
        Task edit operation using put method with rest framework, where you can edit task details, reschedule task accordingly
        """
        label = request.POST.getlist('label')
        image = request.FILES.get('image')
        to_do = ToDo.objects.get(id=pk)
        serializer = ToDoSerializer(instance=to_do, data=request.data)
        if serializer.is_valid():
            serializer_saved = serializer.save(user=request.user, image=image)
            serializer_saved.slug = slugify(serializer_saved.title)
            serializer_saved.save()
            if serializer_saved.reminds_on != None:
                serializer_saved.reminder = True
                serializer_saved.save()
                countdown = (serializer_saved.reminds_on - datetime.now(timezone.utc)).total_seconds()
                task = schedule_todo.apply_async(args=[serializer_saved.id, request.user.id], countdown=countdown)
                serializer_saved.task_id = task
                serializer_saved.save()
            task = ToDo.objects.get(id=serializer_saved.pk)
            task.label.clear()
            task.label.add(*label)

            data = {"response": "success", 'slug': task.slug}
            messages.success(request, "Task edited successfully!!!")
        else:
            data = {"response": "error"}
            messages.error(request, "Cannot edit task")
        return Response(data)

    def delete(self, request, pk):
        """
        Task deletion using delete method with rest framework
        """
        to_do = ToDo.objects.get(id=pk)
        to_do.delete()
        data = {"response": "success"}
        messages.success(request, "Task deleted successfully!!!")
        return Response(data)


class LabelCrudOperation(APIView):
    def post(self, request, pk=None):
        """
        Creating label with given label title
        """
        serializer = LabelSerializer(data=request.data)
        if serializer.is_valid():
            serializer_saved = serializer.save(user=request.user)
            serializer_saved.slug = slugify(serializer_saved.label_title)
            serializer_saved.save()
            messages.success(request, "New label created successfully!!!")
        else:
            messages.error(request, "Cannot create label")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    def get(self, request, slug):
        """
        displaying task related to given label
        """
        label = Label.objects.get(slug=slug)
        to_do_with_label = ToDo.objects.filter(label=label)
        data = {'label_details': label, 'to_do_list': to_do_with_label, "title": "Label : " + label.label_title}
        return render(request, 'label.html', data)

    def put(self, request, pk):
        """
        Editing the label title using put method
        """
        data = request.data
        label = Label.objects.get(id=pk)
        serializer = LabelSerializer(instance=label, data=data)
        if serializer.is_valid():
            label_saved = serializer.save()
            label_saved.slug = slugify(label_saved.label_title)
            label_saved.save()
            data = {"response": "success", 'slug': label_saved.slug}
            messages.success(request, "Label edited successfully!!!")
        else:
            data = {"response": "error"}
            messages.error(request, "Cannot edit label")
        return Response(data)

    def delete(self, request, pk):
        """
        deleting label
        """
        label = Label.objects.get(id=pk)
        label.delete()
        data = {"response": "success"}
        messages.success(request, "Label deleted successfully!!!")
        return Response(data)
