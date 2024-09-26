#!/bin/bash

# Check for the --without-nginx flag
nginx=true
if [[ " $@ " =~ " --without-nginx " ]]; then
    nginx=false
fi

# Start the migration process
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input --clear

touch /app/logs/gunicorn.log
touch /app/logs/access.log
touch /app/logs/nginx-error.log
touch /app/logs/nginx-access.log

# Start nginx
if [ "$nginx" = true ] ;
then
  echo Starting nginx.
  nginx -g 'daemon on;'
fi

# Set number of workers based on the environment
env="${ENV:-PREVIEW}"
worker=4
if [ "$env" = "PROD" ];
then
  worker=8
else
  worker=4
fi

# Watch Gunicorn logs
tail -n 0 -f /app/logs/gunicorn.log &

# Start Gunicorn
echo Starting Gunicorn.
exec gunicorn --config gunicorn.conf.py myapp.wsgi:application
