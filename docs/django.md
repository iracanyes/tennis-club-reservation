# Django


## Install Django

````bash
$ cd /path/to/project_dir/django_project_dir
$ python -m venv .venv


# Isolate Python dev environment in this terminal
# On Windows
$ source .venv/Scripts/activate
# On Unix OS
$ source .venv/bin/activate

# Install Django
$ pip install Django

````

## Create a project


Create a project inside a directory

````bash
$ cd [project_name]/
$ django-admin startproject backend .
````

### Run project

````bash
$ python manage.py runserver
````

## Directory Architecture

- Templates : Describe the presentation to return.
- Views : Function or method that take HTTP requests as arguments, query the model, send data to templates,
and return the result
- Urls : Django provides a way to navigate. Urls are associated with the corresponding responder View
- Models : A model is the single, definitive source of information about your data.

## Templates (same as View in MVC)
Describe the presentation to return.

````html
<h1>My home</h1>
<p>My name is {{ firstname + " " + lastname }} </p>
<p>Date : {{ current_date_time }}. </p>
````

#### Views (same as Controller in MVC)
Function or method that take HTTP requests as arguments, query the model, send data to templates,
and return the result

````python
from django.shortcuts import render
from datetime import datetime


def home(request):
  return render(
    request, 
    'home.html', 
    {
      'current_date_time': datetime.now(),
      'firstname' : 'Py',
      'lastname' : 'Thon'
    }
  )
````

#### URLs

Django provides a way to navigate.
Urls are associated with the corresponding responder View

````python
from django.contrib import admin
from django.urls import path, re_path
from my_app.views.home import home
from tcr_backend.views.login import login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    re_path('^login/$', login, name='login'),
]
````

## Models 
- [Django - Models](https://docs.djangoproject.com/en/6.0/topics/db/models/)
- Model field options : [](https://docs.djangoproject.com/en/6.0/ref/models/fields/#)
- Full documentation : [Django - Model reference](https://docs.djangoproject.com/en/6.0/ref/models/)

A model is the single, definitive source of information about your data. 
It contains the essential fields and behaviors of the data you’re storing. 
Generally, each model maps to a single database table.

The basics:
- Each model is a Python class that subclasses django.db.models.Model.
- Each attribute of the model represents a database field.
- With all of this, Django gives you an automatically-generated database-access API; see Making queries.


### Models directory
models can be declared inside models directory, 


first create models directory
````bash
$ mkdir -p /path/to/project_dir/django_app_name/models && cd $_
$ touch __init__.py
````
Now, you can define your model's classes inside the directory,
Django ORM will looks for app's models inside 'app.models', you will need to import them inside ``models/__init__.py``
`````python
# __init__.py

from .yourClass import YourClass
from .yourNextClass import YourNextClass
`````
Here 2 model's classes defined in corresponding files exists inside ``models`` directory

Here is an sample file with

````python
# yourClass.py
from datetime import datetime
import uuid
from django.db import models


class YourClassName(models.Model):
  class Meta:
    db_table = 'member'
    ordering = ['-lastname','-firstname']

  aftNumber = models.IntegerField()
  firstname = models.CharField(max_length=50)
  lastname = models.CharField(max_length=50)
  gender = models.CharField(max_length=1)
  birth_date = models.DateField()
  created_at = models.DateTimeField(auto_now_add=datetime.now)
  annualFeePaid = models.BooleanField(default=False)
````


### Models - Inheritance

#### Abstract Base Classes

An abstract base class is a model that is not meant to be used directly to create database tables. 
Instead, it provides common fields or methods that other models can inherit.

Example:
````python
from django.db import models


class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Student(CommonInfo):
    grade = models.CharField(max_length=10)


class Teacher(CommonInfo):
    subject = models.CharField(max_length=100)
````
In this example, both Student and Teacher models inherit the name 
and created_at fields from the CommonInfo abstract base class. 
This means that Student and Teacher models will have these fields without having to define them again.

#### Multi-Table Inheritance

With multi-table inheritance, each model in the inheritance chain creates its own table in the database. 
This is useful when you want to extend a model with additional fields but still need to keep the original table.

Example:
````python
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()


class Employee(Person):
    job_title = models.CharField(max_length=100)
````

Here, Person has its own table, and Employee has its own table that links back to the Person table. 
The Employee model extends Person by adding the job_title field.

#### Proxy Models

Proxy models do not create new tables. Instead, they allow you to change the behavior of an existing model without altering the model’s fields.

Example:
````python
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.name}, {self.age} years old"


class PersonProxy(Person):
    class Meta:
        proxy = True
        ordering = ['name']

    def get_uppercase_name(self):
        return self.name.upper()
````
In this example, PersonProxy is a proxy model that inherits from Person. 
It changes the default ordering of Person objects and adds a new method, get_uppercase_name, 
without changing the Person model itself.

### Migrations

````bash
$ python manage.py makemigrations
$ python manage.py migrate []
````