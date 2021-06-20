from django.urls.conf import path
from . import views

urlpatterns = [
    path('test', views.hello_world, name='test'),
    #path('projects/', views.ProjectList.as_view()),
    #path('projects/<int:pk>/', views.ProjectDetail.as_view()),
    path('projects/', views.GenericProjectList.as_view()),
    path('projects/<int:pk>/', views.GenericProjectDetail.as_view()),
    path('tasks/', views.GenericTasktList.as_view()),
    path('tasks/<int:pk>/', views.GenericTasktDetail.as_view()),

    path('projecttasks/<int:pk>/', views.ProjectTasksDetail.as_view()),
]