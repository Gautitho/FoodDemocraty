# Standard / external libraries
import os
import sys
import pathlib
import toml

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

# External modules
sys.path.append(os.path.join(BASE_DIR, '..'))
import xpt_utils as xu

# Internal modules

# Setting default behavior of errors
xu.ERROR_SEVERITY    = "EXCEPTION"
xu.ERROR_PRINT_TRACE = True

# Getting application configuration
xu.check_condition(os.path.exists(os.path.join(BASE_DIR, 'django.conf')), "Missing configuration file django.conf !")
conf_dict = toml.load(os.path.join(BASE_DIR, 'django.conf'))

SECRET_KEY                  = conf_dict['secret_key']           # SECURITY WARNING: keep the secret key used in production secret!
DEBUG                       = conf_dict['debug_en']             # SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS               = conf_dict['allowed_host_list']
CSRF_TRUSTED_ORIGINS        = conf_dict['csrf_trusted_origin_list']
DB_NAME                     = conf_dict['db_name']
DB_PASSWORD                 = conf_dict['db_password']
DB_HOST                     = conf_dict['db_host']
DB_PORT                     = conf_dict['db_port']
SITE_BASE_URL               = conf_dict['site_base_url']

# MODEL_PERMISSION defines the usefull informations the requester want to access
# + 0 : Only model ID
# + 1 : Some model identification informations
# + 2 : Minimal informations requested by a requester
# + 3 : Informations
# + 4 : Informations
# + 5 : Debug informations
MODEL_DEFAULT_INFO_LEVEL        = 4

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'FoodDemocraty',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Main.wsgi.application'

DATABASES = {
    'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': DB_NAME,
          'USER': f'{DB_NAME}_admin',
          'PASSWORD': DB_PASSWORD,
          'HOST': DB_HOST,
          'PORT': DB_PORT
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL  = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': None,
}

STATIC_SRC_DIR  = os.path.join('..', 'static')

if DEBUG:
  import logging
  logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s %(message)s')