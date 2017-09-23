# Python Code Analyzer
## How to run
### Installing the dependencies
To install the dependencies, you need python and pip installed. 

From the /staticCodeAnalyzer/ run
```
pip3 install -r requirements.txt
```
### Running the tests
To run the tests and the project you need django installed.
Before you run the project, you can run the tests with a command
```
./manage.py tests
```
### Running the app
```
./manage.py runserver
```
Then the application is ready at localhost:8000

## About the project
### Basic functionality
This is a simple web application that allows the user to analyze the python files.

####Adding the project
On the main page, the user can type in the url of the github project. Then, several actions 
are fired.
* First, the application checks whether  the provided url is correct by pinging the github API and checking the response code.
* If the url is correct, a RepositoryManager is created. 
* Application uses a model query to check whether the project is already in the database. If it's not, a new
Project is created and saved. Then, the user is redirected to the project site.
####Project page
After adding a new Project or clicking on an existing one on the main page list, the user
is redirected to the Project page. It shows the basic info about the Project and Reports connected to the Project.
It also allows the user to choose Report options, clone the project and generate a new Report.

#### Cloning the project
* A new instance of RepositoryManager is created. 
* Checking if there already is a directory for this repository url. If it's not, a fresh clone is
made.
* If the project has already been cloned, we ping the github API again to get the latest commit date. 
Then, we compare if it's later than the last commit date in the cloned repo on our server. 
This way, we can only clone a project again if there are any new changes.

#### Generating the report
* User can choose what kind of errors and warnings they want to include in the report.
* Parsing flake options and creating a new instance of ReportManager. 
* Checking if there is a report that has the same flake options and there haven't been any
new changes since generating the last report. 
* Checking if cloning the project is needed - we want to generate a report basing on the 
newest data.
* If the project had to be cloned again, we update the Project in the database.
* Creating the report starts with cleaning the cloned project directory - we remove all non-Python files
and redundant directories.
* If the main report folder has not been created yet, we create it. 
* Preparing the main txt report file.
* For each python file in the project dir, flake is run and the output is saved to the dictionary.
* The txt report file is saved and a new Report object is saved to database.

#### Displaying the report
* If there is a txt file with a provided by the Report object path, we parse it and pass
the HTML output to the report.html file
* If it's no longer on the server, we display a message that the Report is no longer available
and the Report object is deleted.

### Final notes
Adding comments has not been implemented.
