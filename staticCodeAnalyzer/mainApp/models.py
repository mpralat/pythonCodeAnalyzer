from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=50)
    repository_url = models.URLField()
    last_commit_date = models.DateTimeField()
    cloned_dir_path = models.CharField(max_length=200, default='')


class Report(models.Model):
    date = models.DateField()
    path_to_report = models.CharField(max_length=300, default='')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
