#!/bin/bash
NAME="readthedocs"                                       # Name of the application
DJANGODIR=/readthedocs.org/readthedocs/                  # Django project directory
SOCKFILE=/readthedocs.org/readthedocs/run/gunicorn.sock  # we will communicte using this unix socket                                         # the group to run as
NUM_WORKERS=3                                            # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=readthedocs.settings.mysql             # which settings file should Django use
DJANGO_WSGI_MODULE=readthedocs.wsgi                  # WSGI module name

echo "Starting $NAME as `whoami`"

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-