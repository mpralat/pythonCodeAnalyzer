from django.shortcuts import render
from git import Repo
import os
import shutil
# Create your views here.
from django.http import HttpResponse


def index(request):
    clone_repo(request)
    return render(request, 'index.html')


def clone_repo(request):
    url = 'https://github.com/mpralat/decisionTrees.git'
    project_name = url.split("/")[-1][:-4]
    print(project_name)
    dir_name = 'cloned_repos/' + project_name
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)

    repo = Repo.clone_from(url, dir_name)