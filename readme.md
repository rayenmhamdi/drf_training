# Welcome to Django Rest Framwork Training!

### You will need:
- Python
- VsCode

## Installation

We need to make sure that python is installed properly
```bash
python --version
```

After this we need to install the virtualenv
```bash
pip install virtualenv`
```

Create your project folder
```bash
mkdir drf_training && cd drf_training
```

We need to create our virtual environment, activate it, install packages and freeze them ([virtualenv best practices](venv.md "virtualenv best practices"))

```bash
virtualenv venv
venv\Scripts\activate
pip install django
pip install djangorestframework
pip freeze >> requirements.txt
```

 let's create a project, an app, migrations and a superuser

```bash
django-admin startproject backend_training .
django-admin startapp project 
python manage.py migrate
python manage.py createsuperuser
```

Finally let's start our server
```bash
python manage.py runserver
```

## Bootstrapping

First thing we need to integrate our app, and drf in our project. 
We need to add 'rest_framework' and 'project.apps.ProjectConfig' in the INSTALLED_APPS section in backend_training.settings

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third_parties
    'rest_framework', # <-- This line
    
    #apps
    'project.apps.ProjectConfig' # <-- and this line
]
```

## Our first Endpoint

in backend_training.urls
```python
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('', include('project.urls')), # <-- add this line
    path('admin/', admin.site.urls),
]
```

create the urls.py file under project folder and paste this content
```python
from django.urls.conf import path
from . import views

urlpatterns = [
    path('test', views.hello_world, name='test'),
]
```

in project.views paste this content
```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})
```

and in your browser open this link : http://localhost:8000/test and voilaaa

## Django Models

let's start by creating our models
```python
class Project(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)
    estimation = models.IntegerField(null=False, blank=False)

    def __str__(self) -> str:
        return "Project Name : {}  estimation : {}".format(self.name, self.estimation)


class Task(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    def __str__(self) -> str:
        return "Task Name : {}  related to : {}".format(self.name, self.project.name)
```

And add them to the admin site
```python
from project.models import Project, Task
from django.contrib import admin

# Register your models here.
admin.site.register(Project)
admin.site.register(Task)
```

## API Time

To create an API we need a serializer, a view and a path. 
let's start by the serializer

```python
from rest_framework import serializers
from project.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', "estimation"]
        #fields = '__all__'
```

then the views

```python
class ProjectList(APIView):
    """
    List all projects, or create a new project.
    """
    def get(self, request, format=None):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

and then the urls
```python
path('projects/', views.ProjectList.as_view()),
path('projects/<int:pk>/', views.ProjectDetail.as_view()),
```
## Relations

if your model relation is done correctly the serilizers will be good
```python
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
```

the views are the same as the projects
```python
class GenericTasktList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class GenericTasktDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

and then the paths
```python
path('tasks/', views.GenericTasktList.as_view()),
path('tasks/<int:pk>/', views.GenericTasktDetail.as_view()),
```


## Custom Presentation
the presentation resides in the serializers like this:
```python
class ProjectTasksSerializer(serializers.ModelSerializer):
    #tasks = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    #tasks = serializers.StringRelatedField(many=True)
    #tasks = TaskSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ['id', "name", "tasks"]
```

