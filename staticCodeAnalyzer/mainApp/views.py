from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Project, Report
from django.http import Http404
from django.utils.timezone import now
from .forms import ProjectForm
from . import repository_functions


def index(request):
    project_form = ProjectForm()
    context = {'projects_list': Project.objects.order_by('-last_commit_date'), 'form': project_form}
    return render(request, 'index.html', context)


def add_project(request):
    form = ProjectForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            print('Adding new repository!')
            url = request.POST.get('repository_url')

            repositoryManager = repository_functions.RepositoryManager(url)

            print(repository_functions.is_repo_correct(url))
            if not repository_functions.is_repo_correct(url):
                print("incorrect url")
            else:
                repositoryManager.clone_repo()
                results =  Project.objects.filter(name=repositoryManager.project_name)
                if results.count() > 0:
                    print("Already in db!")
                    project = results.first()
                else:
                    new_project = Project(name=repositoryManager.project_name,
                                          repository_url=repositoryManager.url,
                                          last_commit_date=repositoryManager.latest_commit_date,
                                          cloned_dir_path=repositoryManager.cloned_repo_path)
                    new_project.save()
                    project = new_project
                return HttpResponseRedirect('/' + str(project.id) + '/')
    else:
        return HttpResponseRedirect('/')


def display_project(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        raise Http404("Project does not exist")
    # reports = project.
    return render(request, 'project.html', {'project': project})
