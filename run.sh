#!/bin/bash
python manage.py makemigrations
python manage.py syncdb
echo "from django.contrib.auth.models import User; User.objects.create_superuser('adminuser', 'haven.wang@rackspace.com', 'j3lskj6kja8sd8jh5')" | python manage.py shell
./scripts/gunicorn_start.sh &
nginx -g "daemon off;"
