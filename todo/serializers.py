from .models import Label, ToDo, Collaborator
from rest_framework.serializers import ModelSerializer

class ToDoSerializer(ModelSerializer):
    class Meta:
        model = ToDo
        exclude = ['label', 'image']

class LabelSerializer(ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'

class CollaboratorSerializer(ModelSerializer):
    class Meta:
        model = Collaborator
        fields = '__all__'