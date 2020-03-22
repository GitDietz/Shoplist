import os

# LOG_ROOT = os.path.join(BASE_DIR, 'Logs')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'large': {
            'format': '%(asctime)s  %(levelname)s  %(process)d  %(funcName)s  %(lineno)d  %(message)s  '
        },
        'med': {
            'format': '%(asctime)s  %(levelname)s [%(module)s-%(funcName)s] %(message)s'
        },
        'tiny': {
            'format': '%(asctime)s  %(message)s'
        }
    },
    'handlers': {
        'errors_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'filename': 'Logs/ErrorLoggers.log',
            'formatter': 'large',
        },
        'info_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'filename': 'Logs/InfoLoggers.log',
            'formatter': 'med',
            },
    },
    'loggers': {
        'error_logger': {
            'handlers': ['errors_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'info_logger': {
            'handlers': ['info_file'],
            'level': 'INFO',
            'propagate': False,
            },
        },
    }