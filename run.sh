#!/bin/sh
python ./manage.py syncdb
python ./manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('test', 'test@example.com', 'test')" | python manage.py shell
python ./manage.py runserver 0.0.0.0:8000
