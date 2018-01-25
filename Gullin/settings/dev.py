"""
Django settings for Gullin Backend.

Development Env Settings
"""

from .prod import *

# Set debug to true
DEBUG = True

# Init debug toolbar
# INSTALLED_APPS += ('debug_toolbar',)
# MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False, }

# Set secret to 42
SECRET_KEY = '42'

# Set allowed hosts to all
ALLOWED_HOSTS = '*'

# Set test db
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME'  : os.path.join(BASE_DIR, 'tmp.sqlite3'),
	}
}

# CORS Settings
CORS_ORIGIN_WHITELIST = (
	'localhost:4000',
	'127.0.0.1:4000',
	'localhost:4004',
	'127.0.0.1:4004'
)
