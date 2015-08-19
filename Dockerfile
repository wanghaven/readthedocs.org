FROM ubuntu:14.04
RUN apt-get update &&\
    apt-get install -y nginx texlive wget git python-dev libpq-dev build-essential autoconf libxml2-dev libxslt1-dev libmysqlclient-dev
RUN wget -O $TMP/get-pip.py https://bootstrap.pypa.io/get-pip.py
RUN python $TMP/get-pip.py
RUN pip install --upgrade pip

# Nginx Setup
RUN ln -sf /dev/stdout /var/log/nginx/access.log &&\
    ln -sf /dev/stderr /var/log/nginx/error.log &&\
    chown -R www-data /var/lib/nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Install readthedocs
COPY . /readthedocs.org
WORKDIR /readthedocs.org
RUN pip install -r requirements/deploy.txt
RUN pip install MySQL-python

#Django setup
RUN python manage.py collectstatic --noinput

RUN apt-get install -y texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended
# Start the RTD server
EXPOSE 80
CMD ["/bin/bash", "./run.sh"]
