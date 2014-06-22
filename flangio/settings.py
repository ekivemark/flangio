# Django settings for flangio project.

import os, sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('James T. Kirk', 'jtk@example.com'),
)
SITE_ID = 1
MANAGERS = ADMINS

BASE_DIR = os.path.join( os.path.dirname( __file__ ), '..' )

# Fix up piston imports here. We would normally place piston in 
# a directory accessible via the Django app, but this is an
# example and we ship it a couple of directories up.
DBPATH=os.path.join(BASE_DIR, 'db/db.db')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DBPATH,                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".


# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True


# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'


# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
os.path.join(BASE_DIR, 'sitestatic'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)



#You need to changes this on your system!! You are creating a security holw if you
# dont change it.
SECRET_KEY = 'cw87b^k4+bl#-jj#gf3)%&!^k@fr_j4#p8g@uoyn!ijzmnce1i'



MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
)


AUTHENTICATION_BACKENDS = ('apps.accounts.auth.HTTPAuthBackend',
                           'apps.accounts.auth.EmailBackend',
                           'django.contrib.auth.backends.ModelBackend',
                          'apps.accounts.auth.BasicBackend',)
                           

#Define our Custom User inside accounts
AUTH_USER_MODEL = 'accounts.flangioUser'

#Tell Django social-ath about the custom model
SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL


LOGIN_URL = '/accounts/login'
LOGOUT_URL = '/accounts/logout'
LOGIN_REDIRECT_URL = '/'
MIN_PASSWORD_LEN = 8

ROOT_URLCONF = 'flangio.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'flangio.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    
    # This should always be the last in the list because it is our default.
    os.path.join(BASE_DIR, 'templates'),
    
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
   'django.contrib.auth.context_processors.auth',
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
   )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    
    #flangio applications
    'apps.socialgraph',
    'apps.accounts',
    'apps.search',
    'apps.mongodb',
    'apps.home',
    'apps.dataimport',
    
    #'apps.transaction',
    # 3rd Party
    'django_ses',
    'bootstrapform',
    'localflavor',
)


#flangio-specific Settings --------------------------------------------------

USERS_MUST_EXIST     = True
RESPECT_SOCIAL_GRAPH = False
AUTO_SELF_FOLLOW     = True
ALLOW_UPDATE_TX      = True #If set to  false, no updates are allowed
ALLOW_DELETE_TX      = True
ENFORCE_TIME_SANITY  = False
MAX_TIME_SKEW_MIN    = 5
OTHER_LABELS         = False # If True, use label value from DataLabelMeta instead of default.
#This must be 'LOCAL', 'AWSS3', or '' for not file support
BINARY_STORAGE        = ''
#Global control of output (CSV, XLS).
SORTCOLUMNS= ()
ALPHABETIZE_COLUMNS   = False



#Mongo DB settings
MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017
MONGO_DB_NAME = "flangio"
MONGO_MASTER_COLLECTION = "main"
MONGO_HISTORYDB_NAME = "history"
MONGO_LIMIT = 100
SINCE_ID_FILE = os.path.join(BASE_DIR, 'db/since.id')


ALLOWABLE_TRANSACTION_TYPES = ("text",)

USERTYPE_CHOICES =(('S','Standard'),
                   ('P','Application'),)

PERMISSION_CHOICES=( ('db-all',   'All MongoDB'),
                     ('db-write',  'Write MongoDB'),
                     ('db-read',   'Read MongoDB'),
                     ('create-other-users',  'create-other-users'),   
                     ('create-any-socialgraph', 'create-any-socialgraph'),
                     ('delete-any-socialgraph',  'delete-any-socialgraph'),
                    )



GENDER_CHOICES=(
        ('F','Female'),
        ('M','Male'),
        ('TMTF','Transgender Male to Female'),
        ('TFTM','Transgender Female to Male'),
        ('SRMTF','Sexual Reassignment Mal to Female'),
        ('SRFTM','Sexual Reassignment Female to Male'),
        ('S','System'),
        )


# To enable you local settings create or copy the example
# file found in ./config/settings_[EXAMPLE].py to the same
# directory as settings.py
try:
    from settings_local import *
except ImportError:
    pass
