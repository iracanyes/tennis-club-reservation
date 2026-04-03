# Django


## Install Django

Create a project

````bash
$ cd [project_name]/
$ django-admin startproject backend .
````

## Directory Architecture

### Templates (same as View in MVC)
Describe the presentation to return.

````html
<h1>My home</h1>
<p>My name is {{ firstname + " " + lastname }} </p>
````

### Views (same as Controller in MVC)
Function or method that take HTTP requests as arguments, query the model, send data to templates,
and return the result

### Models 

The model provides data from the database

### URLs

Django provides a way to navigate.
Urls are associated with the corresponding responder View
