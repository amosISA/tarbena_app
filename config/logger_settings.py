LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'logfile': {
            'class': 'logging.FileHandler',
            'filename': 'logs/server.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['logfile'],
        },
    },
}