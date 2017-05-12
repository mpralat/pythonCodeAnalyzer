from django.test import TestCase
from . import repository_functions
import os
import datetime
import mock

# Create your tests here.

class IsRepoCorrectTestCase(TestCase):
    def test_correct_repo_url(self):
        repo_url = 'https://github.com/git/git.git'
        result = repository_functions.is_url_correct(repo_url)
        self.assertTrue(result)

    def test_incorrect_repo_ulr(self):
        repo_url = "https://github.com/no_repo/repo.git"
        result = repository_functions.is_url_correct(repo_url)
        self.assertFalse(result)

    def test_correct_repo_url_no_git_suffix(self):
        repo_url = 'https://github.com/mpralat/notesRecognizer'
        result = repository_functions.is_url_correct(repo_url)
        self.assertTrue(result)


class IsAlreadyClonedTestCase(TestCase):
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.test_project_dir = self.base_dir + "/cloned_repos/test_project_dir"

    def test_non_existent_cloned_repo(self):
        os.makedirs(self.test_project_dir, 0o755)
        result = repository_functions.is_already_cloned(self.test_project_dir)
        os.rmdir(self.test_project_dir)
        self.assertTrue(result)

    def test_existing_cloned_repo(self):
        if os.path.exists(self.test_project_dir):
            os.rmdir(self.test_project_dir)
        result = repository_functions.is_already_cloned(self.test_project_dir)
        self.assertFalse(result)


class GetLastCommitDateFromUrlTestCase(TestCase):
    def test_correct_last_commit_date(self):
        testManager = repository_functions.RepositoryManager("https://github.com/mpralat/PlaneContours")
        true_last_commit_date = datetime.datetime(2016, 11, 12, 19, 32, 38)
        last_commit_date = testManager.latest_commit_date_from_url()
        self.assertEqual(true_last_commit_date, last_commit_date)


class ProcessGithubUrlTestCase(TestCase):
    def test_correct_github_url(self):
        github_url = 'https://github.com/mpralat/PlaneContours'
        expected_result = 'mpralat/PlaneContours'
        self.assertEqual(expected_result, repository_functions.process_github_url(github_url))

    def test_correct_github_url_with_branch(self):
        github_url = 'https://github.com/mpralat/PlaneContours/tree/better_1'
        expected_result = 'mpralat/PlaneContours/tree/better_1'
        self.assertEqual(expected_result, repository_functions.process_github_url(github_url))

