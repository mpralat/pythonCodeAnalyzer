from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=50)
    repository_url = models.URLField()
    last_modified_date = models.DateField()
    report = models.FileField()
