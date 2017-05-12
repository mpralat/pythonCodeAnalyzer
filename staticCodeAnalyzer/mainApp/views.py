from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import Project, Report
from django.http import Http404
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
            url = request.POST.get('repository_url')
            if not repository_functions.is_url_correct(url):
                print("incorrect url")
                return HttpResponseRedirect('/')
            else:
                repositoryManager = repository_functions.RepositoryManager(url)

                results =  Project.objects.filter(name=repositoryManager.project_name)
                if results.count() > 0:
                    print("Already in database!")
                    project = results.first()
                else:
                    new_project = Project(name=repositoryManager.project_name,
                                          repository_url=repositoryManager.url,
                                          last_commit_date=repositoryManager.latest_commit_date,
                                          cloned_dir_path=repositoryManager.cloned_repo_path)
                    new_project.save()
                    project = new_project
                return HttpResponseRedirect('/project/' + str(project.id) + '/')
    else:
        return HttpResponseRedirect('/')


def display_project(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        raise Http404("Project does not exist")
    # reports = project.
    return render(request, 'project.html', {'project': project})

def clone_project(request):
    if request.POST:
        project_id = request.POST.get('project_id')
        print(project_id)
        project = Project.objects.get(pk=int(project_id))
        cloneManager = repository_functions.RepositoryManager(project.repository_url)
        clone_code = cloneManager.clone_repo()
        return HttpResponse(status=clone_code)
