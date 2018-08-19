from .base import *

DEBUG = False

ALLOWED_HOSTS += ['*', ]

SITE_ID = 2

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tarbena_app',
        'USER': 'amos',
        'PASSWORD': 'cd52405f536e5c7a983c965b74895b3c',
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
