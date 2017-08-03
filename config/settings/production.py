"""
Production Settings


- Add django-extensions as app
"""

from .base import *  # noqa

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['example.com', 'localhost',])

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key


# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='xOTp2|`+FRK;CLCfLudr]P}WB&X]1C#@,_yvlZ;j2d,b3aRiAr')


# CACHING
# ------------------------------------------------------------------------------

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}


INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]


# Custom Admin URL, use {% url 'admin:index' %}
ADMIN_URL = env('DJANGO_ADMIN_URL')

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['django_extensions', ]

# Your production stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------

