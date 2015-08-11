FROM alpine
RUN apk --update add python bash git autoconf build-base openssl-dev libevent-dev libffi-dev libxml2-dev libxslt-dev postgresql-dev redis
RUN wget -O $TMP/get-pip.py https://bootstrap.pypa.io/get-pip.py
RUN python $TMP/get-pip.py
RUN pip install --upgrade pip

# Install readthedocs
RUN git clone https://github.com/wanghaven/readthedocs.org.git
WORKDIR /readthedocs.org
RUN pip install -r requirements.txt

# Set up redis
RUN pip install django-redis-cache
RUN pip install psycopg2
RUN pip install pysolr

# Start the RTD server
EXPOSE 8000
CMD ["/bin/bash", "./run.sh"]
