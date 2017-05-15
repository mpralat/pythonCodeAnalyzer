from django.test import TestCase
import os
from . import report_functions
import shutil

class LeaveOnlyPythonFilesTestCase(TestCase):
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.test_project_dir = self.base_dir + "/cloned_repos/test_project/"
        # Populating with some test python files
        os.mkdir(self.test_project_dir, 0o777)
        for i in range (0,3):
            open(os.path.join(self.test_project_dir, "test" + str(i) + ".py"), 'a').close()
        self.report_manager = report_functions.ReportManager(project_name='test_project', flake_options=[])

    def test_deleting_non_python_files(self):
        open(os.path.join(self.test_project_dir, "test1.txt"), 'a').close()
        open(os.path.join(self.test_project_dir, "test1.pdf"), 'a').close()
        path, dirs, files = os.walk(self.test_project_dir).__next__()
        self.assertEqual(len(files), 5)
        self.report_manager.leave_only_python_files()
        path, dirs, files = os.walk(self.test_project_dir).__next__()
        self.assertEqual(len(files), 3)

    def test_deleting_repositories(self):
        subdir_path = os.path.join(self.test_project_dir, "subdir")
        os.mkdir(subdir_path, 0o777)
        open(os.path.join(subdir_path, "test1.txt"), 'a').close()
        open(os.path.join(subdir_path, "outside_file.py"), 'a').close()
        path, dirs, files = os.walk(self.test_project_dir).__next__()
        # There should still be only 3 files in the main directory and one subdirectory.
        self.assertEqual(len(files), 3)
        self.assertEqual(len(dirs), 1)
        self.report_manager.leave_only_python_files()
        path, dirs, files = os.walk(self.test_project_dir).__next__()
        # There should be one more python file in the main directory now.
        self.assertEqual(len(files), 4)
        self.assertEqual(len(dirs), 0)

    def tearDown(self):
        shutil.rmtree(self.test_project_dir)

# class IsLastReportUpToDateTestCase(TestCase):
#     def