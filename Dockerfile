FROM python:3.8

WORKDIR /usr/src/app

RUN pip install pipenv

COPY Pipfile* ./
COPY simple_notes/ .

RUN pipenv install --deploy --system
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

CMD gunicorn simple_notes.wsgi -b 0.0.0.0:$PORT
