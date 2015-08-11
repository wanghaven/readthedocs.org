#!/bin/sh
python ./manage.py syncdb
python ./manage.py migrate
echo "alter user postgres with password 'postgres';" | psql -U postgres -h $DB_PORT_5432_TCP_ADDR -p 5432
python ./manage.py makemigrations
python ./manage.py migrate
python ./manage.py runserver 0.0.0.0:8000
