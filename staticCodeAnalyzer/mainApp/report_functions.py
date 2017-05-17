import datetime
import glob
import os
import subprocess
import shutil
from .models import Report, Project


class ReportManager:
    def __init__(self, project_name, flake_options):
        self.date = datetime.datetime.now()
        self.flake_options = flake_options
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.project_name = project_name
        self.project_dir = self.base_dir + '/cloned_repos/' + self.project_name

    def leave_only_python_files(self):
        '''
        Copies the python files from all of the subdirectories in the main project directory.
        Next, removes files that do not have .py extension.
        Last, it removes all of the subdirectories (except the .git dir).
        :return: 
        '''
        for filename in glob.iglob(self.project_dir + '/**/*.*', recursive=True):
            name, file_extension = os.path.splitext(filename)
            name = name.split('/')[-1]
            if file_extension == '.py':
                new_destination = self.project_dir + '/' + str(name) + file_extension
                os.rename(filename, new_destination)
            else:
                os.remove(filename)

        paths = get_immediate_subdirectories(self.project_dir)
        for path in paths:
            if not path == '.git':
                shutil.rmtree(os.path.join(self.project_dir, path))

    def run_flake(self, file_name):
        '''
        Runs the flake8 command and waits for the output for a single file.
        '''
        command = ['flake8']
        command.append(file_name)
        select_string = '--select=' + ','.join(self.flake_options)
        command.append(select_string)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.stdout.read()
        output = output.splitlines()
        return self.parse_flake_output(output)

    def parse_flake_output(self, flake_output):
        '''
        Parses the flake8 output.
        :param flake_output: array of strings - lines returned by flake8
        :return: A dictionary, where the key is the error code and the value is an array of json objects representing
        each error.
        '''
        flake_dict = {}
        for line in flake_output:
            line = str(line)
            parsed_line = line.split(":")
            line_num = parsed_line[1]
            column_num = parsed_line[2]
            parsed_line = parsed_line[3].split(' ')
            err_code = parsed_line[1]
            comment = ' '.join(parsed_line[1:])
            if not flake_dict.get(err_code):
                flake_dict[err_code] = []
            flake_dict[err_code].append({'line_num': line_num, 'column_num': column_num, 'comment': comment})

        return flake_dict

    def create_whole_report(self):
        '''
        Prepares the flake output for all files and generates the pdf document.
        :return: 
        '''
        # Removing non-python files and creating a directory with reports.
        self.leave_only_python_files()
        reports_dir = os.path.join(self.base_dir, "reports")
        if not os.path.exists(reports_dir):
            os.mkdir(reports_dir)

        date = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        report_name = self.project_name + '_' + date + '.txt'

        # Preparing the txt file with report
        report_full_path = os.path.join(reports_dir, report_name)
        with open(report_full_path, 'w') as report:
            report.write('Project: ' + self.project_name + '\n')
            report.write('Generated: ' + date + '\n\n')
            for pyfile in glob.glob(self.project_dir + '/*.py'):
                report.write('-----------------------------------------------')
                report.write('\nFile: ' + pyfile.split('/')[-1] + '\n')
                d = self.run_flake(pyfile)
                for key, value in d.items():
                    report.write('ERROR CODE:' + key + ' : ' + value[0].get('comment') + '\n')
                    for item in value:
                        report.write('\t\tLine number: ' + item.get('line_num') +
                                     ',\t\tcolumn: ' + item.get('column_num') + '\n')

        return report_full_path

    def is_generating_report_useful(self):
        ''' 
        Gets the latest report from the database and checks if there are any fresh commits in the repository.
        If there are new commits or the user has chosen a different set of options for the
        report, returns True.
        :return: True if the report 
        '''
        project = Project.objects.filter(name=self.project_name).first()
        last_report = Report.objects.filter(project=project.id).order_by('-date').first()
        if last_report:
            # Checking if the options are different:
            if last_report.options:
                options = last_report.options.split(';')
            else:
                options = ''
            if set(options) != set(self.flake_options):
                return True
            else:
                if project.last_commit_date < last_report.date:
                    return False
                else:
                    return True
        else:
            return True


def get_immediate_subdirectories(main_dir):
    '''
    :return: A list of all immediate subdirectories.
    '''
    return [name for name in os.listdir(main_dir)
            if os.path.isdir(os.path.join(main_dir, name))]

