from .base import *

DEBUG = False

ALLOWED_HOSTS += ['*', ]

SITE_ID = 2

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tarbena_app',
        'USER': 'amos',
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        # 'HOST': 'localhost',
        # 'PORT': 3306,
        # 'OPTIONS': {
        #    'sql_mode': 'traditional'
        # },
    }
}