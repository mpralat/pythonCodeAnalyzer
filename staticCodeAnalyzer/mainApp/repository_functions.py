import os
import git
from git import Repo
from urllib.request import urlopen
import json
from datetime import datetime, timedelta

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#TODO class maybe?

def is_repo_correct(repo_url):
    '''
    Checks whether a repository exists and we can clone it. 
    :return: True if the url is correct, False otherwise.
    '''
    print("Checking if the repository is correct")
    g = git.cmd.Git()
    try:
        response = g.ls_remote(repo_url)
    except Exception:
        return False
    return True


def is_already_cloned(project_path):
    '''
    Checks whether a repository has already been cloned.
    :return: True if the project has already been cloned, False otherwise.
    '''
    if not os.path.exists(project_path):
        return False
    return True


def latest_commit_date_from_url(project_name):
    url = 'https://api.github.com/repos/{project}/commits?per_page=1'.format(project=project_name)
    response = urlopen(url).read()
    response_data = json.loads(response.decode())
    # Get the date string from the json
    latest_commit_date = response_data[0]['commit']['committer']['date']
    # Format the string to get the datetime object. Adding +2GMT
    # TODO time shifts
    datetime_object = datetime.strptime(latest_commit_date, '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=1)
    print("url: " + str(datetime_object))
    return datetime_object


def latest_commit_date_from_cloned_repo(project_path):
    repo = Repo(project_path)
    tree = repo.tree()
    latest_date = 0
    for blob in tree:
        date_to_check = repo.iter_commits(paths=blob.path, max_count=1).__next__().committed_date
        if latest_date < date_to_check:
            latest_date = date_to_check
    print("cloned_repo: " + str(datetime.fromtimestamp(latest_date)))
    return datetime.fromtimestamp(latest_date)

def process_github_url(repo_url):
    '''
    Parses the given repository url to get the project path.
    '''
    chunks_array = repo_url.rstrip('.git').rstrip('/').split('/')
    print(chunks_array)
    github_index = chunks_array.index('github.com')
    project_chunks = chunks_array[github_index+1:]
    project_url = '/'.join(project_chunks)
    return project_url

def clone_repo(repo_url):
    '''
    Checks if the repository url is correct. Then, if the project has already been cloned, it checks
    the last commit dates from remote url and the cloned repo we store in our server. If there are any later commits,
    we clone the repo again.
    :return: 
    '''
    if not is_repo_correct(repo_url):
        return False

    full_project_name = process_github_url(repo_url)
    project_name = full_project_name.split('/')[1:]
    project_name = '_'.join(project_name)
    print(project_name)

    cloned_repo_path = base_dir + '/cloned_repos/' + full_project_name.split('/')[-1]
    # If the repo has already been cloned, we check if there were any new commits.
    if is_already_cloned(cloned_repo_path):
        if latest_commit_date_from_url(full_project_name) > latest_commit_date_from_cloned_repo(cloned_repo_path):
            # Cloning the repo again
            os.rmdir(cloned_repo_path)
            Repo.clone_from(repo_url, cloned_repo_path)
            print("Cloned the repo again!")
        else:
            print("No changes detected.")
    else:
        Repo.clone_from(repo_url, cloned_repo_path)
        print("Cloned the repo")
    return True
