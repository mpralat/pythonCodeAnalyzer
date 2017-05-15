from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Project, Report
from django.http import Http404
from .forms import ProjectForm
from . import repository_functions, report_functions
import datetime


def index(request):
    project_form = ProjectForm()
    context = {'projects_list': Project.objects.order_by('-last_commit_date'), 'form': project_form}
    return render(request, 'index.html', context)


def add_project(request):
    print("add project")
    form = ProjectForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            url = request.POST.get('repository_url')
            if not repository_functions.is_url_correct(url):
                print("incorrect url")
                return HttpResponseRedirect('/')
            else:
                repositoryManager = repository_functions.RepositoryManager(url)

                results = Project.objects.filter(name=repositoryManager.project_name)
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

    report_list = Report.objects.filter(project=project)
    return render(request, 'project.html', {'project': project, 'report_list': report_list})


def clone_project(request):
    if request.POST:
        project_id = request.POST.get('project_id')
        print(project_id)
        project = Project.objects.get(pk=int(project_id))
        cloneManager = repository_functions.RepositoryManager(project.repository_url)
        clone_code = cloneManager.clone_repo()
        if clone_code == 201:
            # if the repository has been cloned again, we update the data in db
            project.last_commit_date = cloneManager.latest_commit_date
            project.save()
        return HttpResponse(status=clone_code)


def generate_report(request):
    if request.POST:
        project_id = request.POST.get('project_id')
        project = Project.objects.get(pk=int(project_id))
        flake_options = request.POST.get('flake_options')
        flake_options = [x for x in flake_options if x.isalpha()]
        options = ";".join(flake_options)
        reportManager = report_functions.ReportManager(flake_options=flake_options, project_name=project.name)
        # Checking if the report should be generated again
        if reportManager.is_generating_report_useful():
            report_path = reportManager.create_whole_report()
            # Creating new Report object
            report = Report(date=datetime.datetime.now(), path_to_report=report_path,
                            project=project, options=options)
            report.save()
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=205)


def display_report(request, report_id):
    try:
        report = Report.objects.get(pk=report_id)
    except Report.DoesNotExist:
        raise Http404("Project does not exist")

    # TODO TXT TO PDF, DISPLAY PDF IN HTML
    try:
        with open(report.path_to_report) as f:
            text_content = f.readlines()
    except FileNotFoundError:
        text_content = "<div> Sorry, but the content you are trying to reach has been deleted. " \
                       "Please generate your report again.</div>"
        # If the txt file has been deleted, we delete the report from the database as well.
        report.delete()
        return render(request, 'report.html', {'report': report, 'content': text_content})
    return render(request, 'report.html', {'report': report, 'content': text_content})
