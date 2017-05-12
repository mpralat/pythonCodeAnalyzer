import datetime
import glob
import os
from subprocess import check_call, STDOUT, CalledProcessError
import subprocess

class ReportManager:
    def __init__(self, project_name, flake_options):
        self.date = datetime.datetime.now()
        self.flake_options = flake_options
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.project_name = project_name


    def run_flake(self, file_name):
        '''
        Runs the flake8 command and waits for the output for a single file.
        '''
        command = 'flake8 ' + file_name
        # output = os.system(command)
        p = subprocess.Popen([command], stdout = subprocess.PIPE)
        output = p.stdout.read()
        return output

    def parse_flake_output(self, flake_output):
        for line in flake_output.split('/n'):
            parsed_line = line.split(':')
            line_num = parsed_line[1]
            column_num = parsed_line[2]
            parsed_line = parsed_line[3].split(' ')
            err_code = parsed_line[0]
            comment = ' '.join(parsed_line[1:])
            print(line_num, column_num, err_code, comment)


    def leave_only_python_files(self):
        '''
        Copies the python files from all of the subdirectories in the main project directory.
        Next, removes files that do not have .py extension.
        Last, it removes all of the subdirectories (except the .git dir).
        :return: 
        '''
        project_dir = self.base_dir + '/cloned_repos/' + self.project_name
        for filename in glob.iglob(project_dir + '/**/*.*', recursive=True):
            name, file_extension = os.path.splitext(filename)
            name = name.split('/')[-1]
            if file_extension == '.py':
                new_destination = project_dir + '/' + str(name) + file_extension
                os.rename(filename, new_destination)
            else:
                os.remove(filename)

        paths = get_immediate_subdirectories(project_dir)
        for path in paths:
            if not path == '.git':
                print(path)
                os.rmdir(os.path.join(project_dir,path))



def get_immediate_subdirectories(main_dir):
    '''
    :return: A list of all immediate subdirectories.
    '''
    return [name for name in os.listdir(main_dir)
            if os.path.isdir(os.path.join(main_dir, name))]

man = ReportManager('anncadClassifier', [])
man.leave_only_python_files()
out = man.run_flake('/home/marta/projects/PycharmProjects/staticCodeAnalyzer/staticCodeAnalyzer/cloned_repos/anncadClassifier/anncad.py')
print(man.parse_flake_output(str(out)))