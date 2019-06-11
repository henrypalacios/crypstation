from .base import *

DEBUG = False

#  Indicate where the static files should be placed.
#  This is necessary so that Nginx can handle requests for these items
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

ALLOWED_HOSTS = ['.example.com']