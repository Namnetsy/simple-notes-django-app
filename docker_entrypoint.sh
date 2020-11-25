#!/bin/sh

path_to_env='simple_notes/simple_notes/.env'

# load variables from .env file
SUPERUSER_USERNAME=$(cat $path_to_env | grep SUPERUSER_USERNAME= | cut -d = -f 2)
SUPERUSER_PASSWORD=$(cat $path_to_env | grep SUPERUSER_PASSWORD= | cut -d = -f 2)
DEBUG=$(cat $path_to_env | grep DEBUG= | cut -d = -f 2)

py="pipenv run python"

# run migrations
$py simple_notes/manage.py makemigrations --noinput
$py simple_notes/manage.py migrate --noinput

is_superuser_exists=$($py simple_notes/manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(username='$SUPERUSER_USERNAME').exists())")

# create super user if not exists
if [ $is_superuser_exists = 'False' ]; then
	$py simple_notes/manage.py shell -c "from django.contrib.auth.models import User; user = User.objects.create_user(username='$SUPERUSER_USERNAME', password='$SUPERUSER_PASSWORD', is_superuser=True, is_staff=True)";
fi

# collect static files if DEBUG is turned off
if [ $DEBUG = 0 ]; then
	$py simple_notes/manage.py collectstatic --noinput;
fi

exec "$@"
