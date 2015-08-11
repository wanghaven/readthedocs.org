import os

from .base import *  # noqa
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'have8923',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
        'OPTIONS': {
            'DB': 0,
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        },
    },
}

REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

# Elasticsearch settings.
ES_HOSTS = ['backup:9200', 'db:9200']
ES_DEFAULT_NUM_REPLICAS = 1
ES_DEFAULT_NUM_SHARDS = 5

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_HTTPONLY = False
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
CACHE_BACKEND = 'redis://'

SLUMBER_USERNAME = 'test'
SLUMBER_PASSWORD = 'test'  # noqa: ignore dodgy check
SLUMBER_API_HOST = 'http://localhost:8000'
# GROK_API_HOST = 'http://localhost:5555'
PRODUCTION_DOMAIN = 'localhost:8000'

WEBSOCKET_HOST = 'websocket.localhost:8088'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

DONT_HIT_DB = False
NGINX_X_ACCEL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CELERY_ALWAYS_EAGER = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
FILE_SYNCER = 'readthedocs.privacy.backends.syncers.LocalSyncer'

# For testing locally. Put this in your /etc/hosts:
# 127.0.0.1 test
# and navigate to http://test:8000
CORS_ORIGIN_WHITELIST = (
    'test:8000',
)

# allauth settings
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

if not os.environ.get('DJANGO_SETTINGS_SKIP_LOCAL', False):
    try:
        from local_settings import *  # noqa
    except ImportError:
        pass
