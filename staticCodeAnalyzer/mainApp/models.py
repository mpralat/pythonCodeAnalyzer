from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=50)
    repository_url = models.URLField()
    last_commit_date = models.DateTimeField()
    cloned_dir_path = models.CharField(max_length=200, default='')


class Report(models.Model):
    date = models.DateField()
    pdf_file = models.FileField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
