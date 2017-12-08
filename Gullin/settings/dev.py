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
