import copy
import gunicorn
from config.settings import LOGGING as BASE_LOGGING_CONFIG

gunicorn.SERVER_SOFTWARE = 'Server'
keepalive = 40

LOGGING = copy.deepcopy(BASE_LOGGING_CONFIG)

GUNICORN_LOGGERS = {
    'gunicorn': {
        'handlers': ['console'],
        'propagate': False,
        'level': 'INFO',
    },
    'gunicorn.error': {
        'handlers': ['console'],
        'propagate': False,
        'level': 'INFO',
    },
    'gunicorn.access': {
        'handlers': ['console'],
        'propagate': False,
        'level': 'INFO',
    }
}

LOGGING['loggers'].update(GUNICORN_LOGGERS)
logconfig_dict = LOGGING
