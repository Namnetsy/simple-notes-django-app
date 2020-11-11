# Simple Notes Django App
A simple note taking application written using python's django web framework.

## Features
 - Write notes using a keyboard driven WYSIYWG editor
 - Orginize notes into notebooks
 - Export notes as PDF files
 - Share your notes via a unique link

# Installing using Docker Compose
Clone repo & create .env file from .env.example
```
$ git clone https://github.com/Namnetsy/simple-notes-django-app 
$ cd simple-notes-django-app
$ cp simple_notes/simple_notes/.env.example simple_notes/simple_notes/.env
```
Note: You may want to edit .env file to sepcify SECRET_KEY and some other information.

Build & Run the app:
```
$ docker-compose up
```
Note: By default it builds the simple notes image with DEBUG=1 which installs dev dependencies.

If you don't want dev dependencies then build it this way & run as shown above:
```
$ docker-compose build --build-arg DEBUG=0
```

# Uninstalling
Remove stopped containers & built image:
```
$ docker-compose rm -f
$ docker rmi simple-notes-django-app_web
```

Remove created volumes:
```
$ docker volume prune -f
```
Note: this will also delete other unused volumes besides created by simple notes
