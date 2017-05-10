from django.shortcuts import render
import os

from django.http import HttpResponse
from .models import Project, Report
from django.http import Http404
from django.utils.timezone import now
from .forms import ProjectForm
from . import repository_functions

def index(request):
    # clone_repo(request)
    project_form = ProjectForm()
    context = {'projects_list': Project.objects.order_by('-last_commit_date'), 'form': project_form}
    return render(request, 'index.html', context)


def add_project(request):
    if request.POST:
        print('Adding new repository!')
        params = request.POST
        print(params)
        url = request.POST.get('repository_url')
        print(url)
    #     TODO check if url is valid

        project_name = repository_functions.clone_repo(url)

        new_project = Project(name=project_name, repository_url=url, last_commit_date=now())
        new_project.save()
        print(new_project.id)
        return HttpResponse(str(new_project.id))
    return None



def display_project(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        raise Http404("Project does not exist")
    # reports = project.
    return render(request, 'project.html', {'project': project})