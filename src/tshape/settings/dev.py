# -*- coding: utf-8 -*-

from tshape.settings.base import *

DEBUG = True

TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("POSTGRES_LOCAL_DB_NAME"),
        'USER': os.environ.get("POSTGRES_LOCAL_DB_USER"),
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
