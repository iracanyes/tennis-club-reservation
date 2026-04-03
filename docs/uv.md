# UV - Python Package & Project manager

## Install

### Windows

````powershell
PS> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
````

### Linux

`````bash
# Using curl
$ curl -LsSf https://astral.sh/uv/install.sh | sh
# Request a specific version
$ curl -LsSf https://astral.sh/uv/0.11.2/install.sh | sh
# Using wget
$ wget -qO- https://astral.sh/uv/install.sh | sh
`````

### Upgrade

When uv is installed via the standalone installer, it can update itself on-demand:
````bash
$ pip install --upgrade uv
````

When another installation method is used, self-updates are disabled. Use the package manager's upgrade method instead. For example, with pip:
````bash
pip install --upgrade uv
````

### Clean up stored data

````bash
$ uv cache clean
````
## Create project 
Create a python project 
````bash
$ uv init [project_name]
$ cd [project_name]
````

or create a project inside a existing directory

````bash
$ mkdir [project_name] && cd $_
$ uv init
````

## Install dependencies

````bash
$ uv add [dependency_name]
````