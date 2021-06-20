from rest_framework import serializers
from project.models import Project, Task

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class ProjectTasksSerializer(serializers.ModelSerializer):
    #tasks = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    #tasks = serializers.StringRelatedField(many=True)
    #tasks = TaskSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ['id', "name", "tasks"]