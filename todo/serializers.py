from .models import Label, ToDo
from rest_framework.serializers import ModelSerializer


class ToDoSerializer(ModelSerializer):
    class Meta:
        model = ToDo
        exclude = ['label', 'image']


class LabelSerializer(ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'
