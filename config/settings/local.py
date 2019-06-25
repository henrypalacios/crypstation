from .base import *

DEBUG = True

SECRET_KEY = '-5og^w3c^tcsp^n)9wk+2bvb(2j_vm=8o38j8t8@r4q%b&j=y_'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = ['localhost', 'crypstation.test']

# to execute tasks locally synchronous
# CELERY_ALWAYS_EAGER = True

