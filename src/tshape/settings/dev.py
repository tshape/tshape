# -*- coding: utf-8 -*-

from tshape.settings.base import *

DEBUG = True

TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test',
        'USER': os.environ.get('PGUSER'),
		'PASSWORD': os.environ.get('PGPASSWORD'),
    	'HOST': '127.0.0.1',
        'PORT': 5432,
    }
}
