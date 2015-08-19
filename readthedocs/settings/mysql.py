import os

from .base import *  # noqa
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysql',
        'USER': 'mysql',
        'PASSWORD': 'mypass',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': (os.environ.get('CACHE_PORT_6379_TCP_ADDR') or 'localhost') + ':6379',
        'OPTIONS': {
            'DB': 0,
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        },
    },
}

REDIS = {
    'host': os.environ.get('CACHE_PORT_6379_TCP_ADDR', 'localhost'),
    'port': 6379,
    'db': 0,
}

DEBUG = False
TEMPLATE_DEBUG = False

# Elasticsearch settings.
ES_HOSTS = ['localhost:9200']
ES_DEFAULT_NUM_REPLICAS = 1
ES_DEFAULT_NUM_SHARDS = 5

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_HTTPONLY = False
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
CACHE_BACKEND = 'redis://'

SLUMBER_USERNAME = 'adminuser'
SLUMBER_PASSWORD = 'j3lskj6kja8sd8jh5'  # noqa: ignore dodgy check
SLUMBER_API_HOST = 'http://localhost:8000'
PRODUCTION_DOMAIN = 'localhost:8000'

WEBSOCKET_HOST = 'websocket.localhost:8088'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

DONT_HIT_DB = False
NGINX_X_ACCEL_REDIRECT = True

# If you are deployed behind a load-balancer or reverse-proxy server, and the
# ``Strict-Transport-Security`` header is not being added to your responses,
# it may be because Django doesn't realize that it's on a secure connection;
# you may need to set the :setting:`SECURE_PROXY_SSL_HEADER` setting.
#SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

#CELERY_ALWAYS_EAGER = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
FILE_SYNCER = 'readthedocs.privacy.backends.syncers.LocalSyncer'

# allauth settings
#ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

# This is where Nginx will serve the static assets
STATIC_ROOT = os.path.join(os.getcwd(), "static/")


if not os.environ.get('DJANGO_SETTINGS_SKIP_LOCAL', False):
    try:
        from local_settings import *  # noqa
    except ImportError:
        pass
