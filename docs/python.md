# Python project

## Installation

Download and install Python : [Install Python 3.14 on Windows](https://www.python.org/ftp/python/3.14.3/python-3.14.3-amd64.exe)

You can also install [Python Install Manager](https://www.python.org/ftp/python/pymanager/python-manager-26.1.msix)

### Environment variables

Find the installation folder
````bash
$ which python
````

Create the environment variables if not already done
On Windows OS, you must add Python DLLs and Lib folders to PYTHONPATH
On Linux, only the lib folder is needed
````text
PYTHONPATH=C:\path\to\python_directory\Python314\Lib;C:\path\to\python_directory\Python314\DLLs
PYTHONHOME=C:\path\to\python_directory\Python314
````


Next, Add the path to python executable into the environment variables PATH
````text
C:\tools\dev\python\Python314
````

## Create Project

Create the project root directory

````bash
$ mkdir tsr/backend && cd $_
````
### Python - Virtual environment

#### Create a virtual environment

In order to isolate python environment, we create a virtual environment folder, using the module ``venv`` usually in ``~/.virtualenv`` ou ``~/.venv``
with the following command with the python version of your choice :
Notation: python -m venv [venv_name]

````shell
# Here we create a virtual environment for Odoo app in our home directory
$ cd ~
$ mkdir .venv && cd $_ 
$ python -m venv odoo-env
````
You can also the create a dedicated virtual environment for each project 

````bash
$ mkdir [project_name] && cd $_
$ py -m venv .venv 

````


##### Activate a virtual environmentython environment
using the script located in your virtualenv f
You can connect your shell to the isolated polder :

````shell
# On Windows
$ [venv_foldername]\Scripts\activate

# On Unix
$ source [venv_folder_name]/bin/activate
````

Your shell command line descriptor should change to mark the connection to the virtual environment,
you can now install modules inside your virtual environment:

````shell

(odoo-env) ...$ pip install phonenumbers
````

The newly installed modules should be located in ``~/.venv/odoo-env/Lib/site-packages/``

For more information: [Python - Virtual environment](https://docs.python.org/fr/3/tutorial/venv.html)

##### Desactivate a virtual environment

````shell
(odoo-env) $ deactivate
````

## Install dependencies

We add all project's dependencies inside the ``requirements.txt``
````text
djangorestframework=3.12.4
````
Next, we install the dependencies
````shell
pip install -r requirements.txt
````

