FROM python:3.8

ARG DEBUG=1

ENV DEBUG=$DEBUG
ENV PORT=5000

WORKDIR /usr/src/app

RUN pip install pipenv

# copy pipfiles & install dependencies including dev ones if DEBUG = 1
COPY Pipfile* ./
RUN pipenv install $(if [ $DEBUG = 1 ]; then echo '--dev'; else echo '--deploy'; fi) --ignore-pipfile

# copy source code to working directory
COPY . ./

# enable hot reloading if DEBUG = 1
CMD cd simple_notes; pipenv run gunicorn $(if [ $DEBUG = 1 ]; then echo '--reload'; fi) simple_notes.wsgi -b 0.0.0.0:$PORT

ENTRYPOINT ["./docker_entrypoint.sh"]
