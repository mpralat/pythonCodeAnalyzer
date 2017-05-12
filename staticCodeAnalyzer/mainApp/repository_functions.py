import os
import git
from git import Repo
from urllib.request import urlopen
import json
from datetime import datetime, timedelta

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# TODO class maybe?

class RepositoryManager:
    def __init__(self, base_url):
        self.url = base_url
        self.project_name_with_author = process_github_url(self.url)
        project_name = self.project_name_with_author.split('/')[1:]
        self.project_name = '_'.join(project_name)
        self.cloned_repo_path = base_dir + '/cloned_repos/' + self.project_name_with_author.split('/')[-1]
        self.cloned_before = False
        self.latest_commit_date = None

    def clone_repo(self):
        '''
        Checks if the repository url is correct. Then, if the project has already been cloned, it checks
        the last commit dates from remote url and the cloned repo we store in our server. If there are any later commits,
        we clone the repo again.
        :return: 
        '''
        # If the repo has already been cloned, we check if there were any new commits.
        print("Cloning the repository...")
        url_date = self.latest_commit_date_from_url()
        self.latest_commit_date = url_date

        if is_already_cloned(self.cloned_repo_path):
            repo_date = self.latest_commit_date_from_cloned_repo()
            if url_date > repo_date:
                # Cloning the repo again
                os.rmdir(self.cloned_repo_path)
                Repo.clone_from(self.url, self.cloned_repo_path)
                self.cloned_before = True
                print("Cloned the repo again!")
            else:
                self.cloned_before = True
                print("No changes detected. Not cloning again.")
        else:
            Repo.clone_from(self.url, self.cloned_repo_path)
            print("Cloned the repo for the first time.")
        return True

    def latest_commit_date_from_url(self):
        url = 'https://api.github.com/repos/{project}/commits?per_page=1'.format(project=self.project_name_with_author)
        response = urlopen(url).read()
        response_data = json.loads(response.decode())
        # Get the date string from the json
        latest_commit_date = response_data[0]['commit']['committer']['date']
        # Format the string to get the datetime object. Adding +2GMT
        # TODO time shifts
        datetime_object = datetime.strptime(latest_commit_date, '%Y-%m-%dT%H:%M:%SZ') \
            # + timedelta(hours=2)
        print("url: " + str(datetime_object))
        return datetime_object

    def latest_commit_date_from_cloned_repo(self):
        repo = Repo(self.cloned_repo_path)
        tree = repo.tree()
        latest_date = 0
        for blob in tree:
            date_to_check = repo.iter_commits(paths=blob.path, max_count=1).__next__().committed_date
            if latest_date < date_to_check:
                latest_date = date_to_check
        final_date = datetime.fromtimestamp(latest_date)
        return final_date


# HELPER FUNCTIONS

def is_url_correct(repo_url):
    '''
    Checks whether a repository exists and we can clone it. 
    :return: True if the url is correct, False otherwise.
    '''
    print("Checking if the repository url is correct")
    print(repo_url)
    try:
        result = urlopen(repo_url)
    except:
        return False
    if result.code == 200:
        return True
    return False


def is_already_cloned(project_path):
    '''
    Checks whether a repository has already been cloned.
    :return: True if the project has already been cloned, False otherwise.
    '''
    if not os.path.exists(project_path):
        return False
    return True


def process_github_url(repo_url):
    '''
    Parses the given repository url to get the project path.
    '''
    chunks_array = repo_url.rstrip('.git').rstrip('/').split('/')
    print(chunks_array)
    github_index = chunks_array.index('github.com')
    project_chunks = chunks_array[github_index + 1:]
    project_url = '/'.join(project_chunks)
    return project_url
