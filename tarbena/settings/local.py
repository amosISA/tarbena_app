from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tarbena',
        'USER': 'root',
        'PASSWORD': ''
    }
}

INSTALLED_APPS += ['debug_toolbar', ]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

INTERNAL_IPS = ('127.0.0.1', )

