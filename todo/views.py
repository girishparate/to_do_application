from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.contrib import messages
from django.http import HttpResponseRedirect
from rest_framework.parsers import FileUploadParser
from .models import *
from .serializers import *
from schedule_task.tasks import schedule_todo, app
from datetime import datetime, timezone
from django.utils.text import slugify



# Create your views here.
class MainDashboard(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main_dashboard.html'

    def get(self, request):
        data = {"title": "To Do Application",
                "tasks": ToDo.objects.filter(user=request.user)
                }
        return Response(data)

    def post(self, request):
        serializer = ToDoSerializer(data=request.data)
        label = request.POST.getlist('label')
        image = request.FILES.get('image')
        if serializer.is_valid():
            
            serializer_saved = serializer.save(user=request.user, image=image)
            serializer_saved.slug = slugify(serializer_saved.title)
            serializer_saved.save()
            if serializer_saved.reminds_on !=None:
                serializer_saved.reminder = True
                serializer_saved.save()
                countdown = (serializer_saved.reminds_on - datetime.now(timezone.utc)).total_seconds()
                task = schedule_todo.apply_async(args=[serializer_saved.id, request.user.id],countdown=countdown)
                serializer_saved.task_id = task
                serializer_saved.save()
            task = ToDo.objects.get(id=serializer_saved.pk)
            task.label.add(*label)

            data = {"response": "success"}
        else:
            data = {"response": "error"}
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class ToDoCrudOperation(APIView):
    def get(self, request, slug):
        to_do = ToDo.objects.get(slug=slug)
        data = {'to_do': to_do}
        return render(request, 'task_detail.html', data)
    
    def put(self, request, pk):
        print(request.data)
        label = request.POST.getlist('label')
        image = request.FILES.get('image')
        to_do = ToDo.objects.get(id=pk)
        serializer = ToDoSerializer(instance=to_do, data=request.data)
        if serializer.is_valid():
            serializer_saved = serializer.save(user=request.user, image=image)
            serializer_saved.slug = slugify(serializer_saved.title)
            serializer_saved.save()
            if serializer_saved.reminds_on !=None:
                serializer_saved.reminder = True
                serializer_saved.save()
                countdown = (serializer_saved.reminds_on - datetime.now(timezone.utc)).total_seconds()
                task = schedule_todo.apply_async(args=[serializer_saved.id, request.user.id],countdown=countdown)
                serializer_saved.task_id = task
                serializer_saved.save()
            task = ToDo.objects.get(id=serializer_saved.pk)
            task.label.clear()
            print(label)
            task.label.add(*label)

            data = {"response": "success", 'slug':task.slug}
        else:
            data = {"response": "error"}
        return Response(data)

    def delete(self, request, pk):
        to_do = ToDo.objects.get(id=pk)
        to_do.delete()
        data = {"response": "success"}
        return Response(data)


class LabelCreation(APIView):
    def post(self, request, pk=None):
        serializer = LabelSerializer(data=request.data)
        if serializer.is_valid():
            serializer_saved = serializer.save(user=request.user)
            serializer_saved.slug = slugify(serializer_saved.label_title)
            serializer_saved.save()
        data = {"response": "success"}
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    def get(self, request, slug):
        label = Label.objects.get(slug=slug)
        to_do_with_label = ToDo.objects.filter(label=label)
        data = {'label_details': label, 'to_do_list': to_do_with_label}
        return render(request, 'label.html', data)
    
    def put(self, request, pk):
        data = request.data
        label = Label.objects.get(id=pk)
        serializer = LabelSerializer(instance=label, data=data)
        if serializer.is_valid():
            label_saved = serializer.save()
            label_saved.slug = slugify(label_saved.label_title)
            label_saved.save()
            data = {"response": "success", 'slug':label_saved.slug}
        else:
            data = {"response": "error"}
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    def delete(self, request, pk):
        label = Label.objects.get(id=pk)
        label.delete()
        data = {"response": "success"}
        return Response(data)
 