"""
Django settings for Gullin Backend.

Production Env Settings

See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/
"""

import os
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = open(os.path.join(BASE_DIR, 'settings/securities/django_secret_key')).read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	# installed packages
	'django_celery_results',
	'corsheaders',
	# customized utils
	'Gullin.utils.rest_framework_jwt',
	# modules
	'Gullin.modules.users',
	'Gullin.modules.companies',
	'Gullin.modules.wallets',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Gullin.urls'
AUTH_USER_MODEL = 'users.User'

TEMPLATES = [
	{
		'BACKEND' : 'django.template.backends.django.DjangoTemplates',
		'DIRS'    : [os.path.join(BASE_DIR, 'templates')],
		'APP_DIRS': True,
		'OPTIONS' : {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'Gullin.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
	'default': {
		'ENGINE'  : 'django.db.backends.mysql',
		'NAME'    : '',
		'USER'    : '',
		'PASSWORD': '',
		'HOST'    : '',
		'PORT'    : ''
	}
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
	{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
	{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
	{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
	{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Set auto redirect to false
APPEND_SLASH = False

# Django Rest Framework Settings
REST_FRAMEWORK = {
	'DEFAULT_PERMISSION_CLASSES'    : (
		'rest_framework.permissions.IsAuthenticatedOrReadOnly',
	),
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'Gullin.utils.rest_framework_jwt.authentication.BaseJSONWebTokenAuthentication',
	),
	'DEFAULT_RENDERER_CLASSES'      : (
		'rest_framework.renderers.JSONRenderer',
	),
	'DEFAULT_PAGINATION_CLASS'      : 'rest_framework.pagination.LimitOffsetPagination',
	'PAGE_SIZE'                     : 100,
}

# Json Web Token Settings
# How to generate RS256 keys:
# > ssh-keygen -t rsa -b 2048 -f jwt_secret.key
# > openssl rsa -in jwt_secret.key -pubout -outform PEM -out jwt_secret.key.pub
JWT_AUTH = {
	'JWT_PUBLIC_KEY'              : open(os.path.join(BASE_DIR, 'settings/securities/jwt_secret.key.pub')).read(),
	'JWT_PRIVATE_KEY'             : open(os.path.join(BASE_DIR, 'settings/securities/jwt_secret.key')).read(),
	'JWT_ALGORITHM'               : 'RS256',

	'JWT_VERIFY_EXPIRATION'       : True,
	'JWT_EXPIRATION_DELTA'        : datetime.timedelta(hours=1),
	'JWT_ALLOW_REFRESH'           : True,
	'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=1),

	'JWT_AUTH_HEADER_PREFIX'      : 'JWT',
	'JWT_AUTH_COOKIE'             : 'gullin_jwt'
}

# GeoIP Path Setting
GEOIP_PATH = os.path.join(BASE_DIR, 'utils/geoip')

# CORS Settings
CORS_ORIGIN_WHITELIST = (
	'http://app.gullin.io',
	'https://app.gullin.io',
)

CORS_ALLOW_HEADERS = (
	'accept',
	'accept-encoding',
	'authorization',
	'content-type',
	'origin',
	'user-agent',
	'x-csrftoken',
	'x-requested-with',
	'cache-control',
	'HTTP_X_XSRF_TOKEN',
	'X-CSRF-TOKEN',
	'XMLHttpRequest',
	'Access-Control-Allow-Origin',
	'Access-Control-Allow-Methods',
	'Access-Control-Allow-Headers',
	'Access-Control-Allow-Credentials',
	'Access-Control-Max-Age'
)

CORS_PREFLIGHT_MAX_AGE = 86400
CORS_ALLOW_CREDENTIALS = True

# AWS Credentials
AWS_ACCESS_KEY_ID = open(os.path.join(BASE_DIR, 'settings/securities/aws_secret_key')).read().splitlines()[0]
AWS_SECRET_ACCESS_KEY = open(os.path.join(BASE_DIR, 'settings/securities/aws_secret_key')).read().splitlines()[1]

# AWS S3 Storage
AWS_S3_HOST = 's3.us-east-1.amazonaws.com'
AWS_STORAGE_BUCKET_NAME = 'gullin-storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS SES Email Service
AWS_SES_REGION_NAME = 'us-east-1'
EMAIL_BACKEND = 'Gullin.utils.send.email.SESBackend'
EMAIL_SEND_FROM = 'Gullin <noreply@gullin.io>'
# Async Email Sending Backend
# TODO
# EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
# CELERY_EMAIL_BACKEND = 'Gullin.utils.send.email.SESBackend'
# CELERY_EMAIL_TASK_CONFIG = {
# 	'name'         : 'djcelery_email_send',
# 	'ignore_result': True,
# 	'queue'        : 'email',
# 	'rate_limit'   : '100/m',
# }

# AWS SNS Message Service
AWS_SNS_REGION_NAME = 'us-east-1'

# Set Max Data Upload Size to 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800

# Set IdentityMind API Endpoint
IDENTITY_MIND_API = ''

# Celery
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_BEAT_SCHEDULE = {
	'check_verification_status': {
		'task'    : 'Gullin.modules.users.tasks.check_verification_status',
		'schedule': 300.0,
	},
}
