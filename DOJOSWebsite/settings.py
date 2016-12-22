from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

import os

###################
# DJANGO SETTINGS #

# Hosts/domain names that are valid; required if DEBUG is False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.241.204.118', '*']

DATEFORMAT = "D, M d"
TIMEFORMAT = 'f A'

# Local time zone; codes: wikipedia
TIME_ZONE = 'America/Los_Angeles'

# If True, Django will timezone-aware
USE_TZ = True

# Language code
LANGUAGE_CODE = 'en'

# Supported languages
LANGUAGES = (
    ('en', _('English')),
)

# Session cookie expire when browser closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SITE_ID = 1

# If False, Django will not load internationalization.
USE_I18N = False
USE_L10N = False

AUTHENTICATION_BACKENDS = ('mezzanine.core.auth_backends.MezzanineBackend',)

# Numeric mode for newly-uploaded files passed to os.chmod.
FILE_UPLOAD_PERMISSIONS = 0o644

#############
# DATABASES #
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        # Set to empty string for localhost.
        'HOST': '',
        'PORT': '',
    }
}

#########
# PATHS #

# Full filesystem path to the project.
PROJECT_APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_APP = os.path.basename(PROJECT_APP_PATH)
PROJECT_ROOT = BASE_DIR = os.path.dirname(PROJECT_APP_PATH)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip('/'))
MEDIA_URL = STATIC_URL + 'media/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip('/').split('/'))
ROOT_URLCONF = '%s.urls' % PROJECT_APP

LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'

# TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, 'templates'),)

# Every cache key prefixed with this value
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_APP

GEOIP_DATABASE = STATIC_ROOT + '/easy_timezones/GeoLiteCity.dat'
GEOIPV6_DATABASE = STATIC_ROOT + '/easy_timezones/GeoLiteCityv6.dat'


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.postgres',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'mezzanine.boot',
    'mezzanine.conf',
    'mezzanine.core',
    'mezzanine.generic',
    'mezzanine.pages',
    'mezzanine.forms',
    'mezzanine.galleries',
    'mezzanine.accounts',

    ### NOT IMPLEMENTED
    # 'mezzanine.blog',
    # 'mezzanine.twitter',
    # 'mezzanine.mobile',
    # 'mailer',
    # 'schedule',
    # 'djconfig',

    ### 3rd party apps
    'request',
    'floppyforms',
    # 'haystack',
    'tracking',
    'friendship',
    'josmessages',
    'cloudinary',
    'embed_video',
    'notification',
    'taggit',

    ### NOT IMPLEMENTED


    ### Custom apps
    'josstaff',
    'josmembers',
    'josprojects',
    'joscourses',
    'josplayground',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                ### TEMPLATE_CONTEXT_PROCESSORS
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.tz',

                'mezzanine.conf.context_processors.settings',
                'mezzanine.pages.context_processors.page',

                'josprojects.context_processors.help_sys',
                'josmessages.context_processors.inbox',
                # 'djconfig.context_processors.config',
            ],
            "builtins": [
                "mezzanine.template.loader_tags",
            ],
        },
    },
]

# Middleware. Order is important; request classes in order, response in reverse order.
MIDDLEWARE = [
    'request.middleware.RequestMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # If localisation: 'django.middleware.locale.LocaleMiddleware',

    'mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware',
    'mezzanine.core.middleware.FetchFromCacheMiddleware',
    'mezzanine.core.middleware.RedirectFallbackMiddleware',
    'mezzanine.core.middleware.SitePermissionMiddleware',
    'mezzanine.core.middleware.TemplateForDeviceMiddleware',
    'mezzanine.core.middleware.TemplateForHostMiddleware',
    'mezzanine.core.middleware.UpdateCacheMiddleware',
    'mezzanine.core.request.CurrentRequestMiddleware',
    'mezzanine.pages.middleware.PageMiddleware',
    # If using SSL settings: 'mezzanine.core.middleware.SSLRedirectMiddleware',

    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'tracking.middleware.VisitorTrackingMiddleware',
]

########################
# DJANGO DEBUG TOOLBAR #
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

#########################
# OPTIONAL APPLICATIONS #

# Store as package names as they may change.
PACKAGE_NAME_FILEBROWSER = 'filebrowser_safe'
PACKAGE_NAME_GRAPPELLI = 'grappelli_safe'

OPTIONAL_APPS = (
    'debug_toolbar',
    'django_extensions',
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
    ### Not working: 'compressor',
)

###########
# PROFILE #
ACCOUNTS_NO_USERNAME = True
ACCOUNTS_PROFILE_VIEWS_ENABLED = True
ACCOUNTS_PROFILE_MODEL = 'josmembers.JOSProfile'
ACCOUNTS_PROFILE_FORM_CLASS = 'josmembers.forms.JOSProfileForm'
# ACCOUNTS_VERIFICATION_REQUIRED = False
# ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS = ()

######################
# TRACKER & REQUEST  #
TRACK_AJAX_REQUESTS = True
TRACK_PAGEVIEWS = True
TRACK_REFERER = True
TRACK_QUERY_STRING = True

REQUEST_LOG_IP = False
REQUEST_TRAFFIC_MODULES = (
    'request.traffic.UniqueVisitor',
    'request.traffic.UniqueVisit',
    'request.traffic.User',
    'request.traffic.UniqueUser',
    'request.traffic.Hit',
    'request.traffic.Ajax',
    'request.traffic.Error',
)

REQUEST_PLUGINS = (
    'request.plugins.ActiveUsers',
    'request.plugins.TopReferrers',
    'request.plugins.LatestRequests',
    'request.plugins.TopPaths',
    'request.plugins.TopErrorPaths',
)

##################
# OTHER SETTINGS #
TAGGIT_CASE_INSENSITIVE = True

JQUERY_FILENAME = 'jquery-1.8.3.min.js'

#########
# EMAIL #
# EMAIL_SUBJECT_PREFIX = 'Join Our Story'
# SERVER_EMAIL = EMAIL_HOST_USER = 'joinus@joinourstory.com'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_PASSWORD = '4Primetime!'
# EMAIL_PORT = 587
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'joinus@joinourstory.com'

#########
# FORUM #
# from spirit.settings import *

##################
# LOCAL SETTINGS #
# Instead of 'from .local_settings import *', we use exec for full access
f = os.path.join(PROJECT_APP_PATH, 'local_settings.py')
if os.path.exists(f):
    exec (open(f, 'rb').read())

####################
# DYNAMIC SETTINGS #
# set_dynamic_settings() rewrites global  defaults.
try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())

DEBUG = False

### COMMENT IN TO GET DJANGO DEBUG TOOLBAR ###
def show_toolbar(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}

DEBUG = True
