from .base import *

DEBUG = False

ALLOWED_HOSTS = tuple(env.list('ALLOWED_HOSTS', default=[]))