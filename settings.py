# Django settings for laresumex project.

#CUSTOM VARS
FULL_PATH = "/home/sdrc9/public_html/laresumex";
RESUME_STORE = "%s/STORE/" % (FULL_PATH);
RESUME_FORMAT = "%s/templates/moderncv" % (FULL_PATH);
#ROOT = "/laresumex"
ROOT=''

#DEFAUT VARS

DEBUG =True 
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Apoorva', 'ascoolas.apoorva@gmail.com'),
    ('Knight Samar','knightsamar@gmail.com'),
    ('Ashwini','ashwini7security@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'laresumex',                      # Or path to database file if using sqlite3.
        'USER': 'ashwini',                      # Not used with sqlite3.
        'PASSWORD': 'tangobingo7',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Kolkata'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = FULL_PATH + "/media";

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://localhost/~sdrc9/laresumex/media';

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '~media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '9jf+y@qgarz#yev+g$x(^oo=7cv2^-@v$62@#3*iz9q6*4#!asdu123fo'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'laresumex.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    FULL_PATH + '/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
     'django.contrib.admin',
    #Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'laresumex.student_info',
    'laresumex.generate_resume',
    'laresumex.company',
    'laresumex.ldap_login',
    'laresumex.jobposting',
)
