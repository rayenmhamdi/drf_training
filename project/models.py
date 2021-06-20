from django.db import models

# Create your models here.

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