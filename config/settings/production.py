import socket
from .base import *

DEBUG = False

ALLOWED_HOSTS += ['*', ]

SITE_ID = 3

HOSTNAME = socket.gethostname()
if HOSTNAME == 'servidor':
    with open('/home/admin/files/django_prod_secret_dbpw.txt') as f:
        DB_PW = f.read().strip()
else:
    from .django_secrets import PRODUCTION_DB_PASSWORD
    DB_PW = PRODUCTION_DB_PASSWORD

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tarbena_app',
        'USER': 'amos',
        'PASSWORD': DB_PW,
        # 'HOST': 'localhost',
        # 'PORT': 3306,
        # 'OPTIONS': {
        #    'sql_mode': 'traditional'
        # },
    }
}

# Add logger to production for debugging
try:
    from config.logger_settings import *
except Exception as e:
    pass
