# Python project

## Installation

Download and install Python : [Install Python 3.14 on Windows](https://www.python.org/ftp/python/3.14.3/python-3.14.3-amd64.exe)

You can also install [Python Install Manager](https://www.python.org/ftp/python/pymanager/python-manager-26.1.msix)

### Environment variables
Create the environment variables if not already done
````text
PYTHONPATH=C:\tools\dev\python\Python314\Lib
PYTHONHOME=C:\tools\dev\python\Python314
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
### Virtual environment

Create a virtual environment to isolate our package dependencies locally

`````bash
$ py -m venv .venv
`````
Activate the virtual environment to isolate all next python command for this terminal
to this virtual environment ()

````bash
source .venv/Scripts/activate
````