from .base import *

DEBUG = False

ALLOWED_HOSTS += ['*', ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tarbena',
        'USER': 'amos',
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        # 'HOST': 'localhost',
        # 'PORT': 3306,
        # 'OPTIONS': {
        #    'sql_mode': 'traditional'
        # },
    }
}