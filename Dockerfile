FROM python:3.8

ARG DEBUG=1
ARG SUPERUSER_USERNAME=root
ARG SUPERUSER_PASSWORD=toor

ENV DEBUG=$DEBUG
ENV PORT=5000

WORKDIR /usr/src/app

RUN pip install pipenv

# copy pipfiles & install dependencies including dev ones if DEBUG = 1
COPY Pipfile* ./
RUN pipenv install $(if [ $DEBUG = 1 ]; then echo '--dev'; else echo '--deploy'; fi) --system

# copy source code to working directory & collect static files if DEBUG = 0
COPY simple_notes/ .
RUN if [ $DEBUG = 0 ]; then python manage.py collectstatic --noinput; fi

# apply migrations
RUN python manage.py migrate

# create superuser
RUN python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser(username='$SUPERUSER_USERNAME', password='$SUPERUSER_PASSWORD')"

# enable hot reloading if DEBUG = 1
CMD gunicorn $(if [ $DEBUG = 1 ]; then echo '--reload'; fi) simple_notes.wsgi -b 0.0.0.0:$PORT
