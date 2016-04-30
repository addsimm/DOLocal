from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

import os

###################
# DJANGO SETTINGS #
###################

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.241.204.118', '*']

DATETIME_FORMAT = "D, M d - fA"

# Local time zone. Choice codes: wikipedia
TIME_ZONE = 'America/Los_Angeles'

# If True, Django will use timezone-aware datetimes.
USE_TZ = True

# Language code
LANGUAGE_CODE = "en"

# Supported languages
LANGUAGES = (
    ('en', _('English')),
)

DEBUG = False

# Whether a user's session cookie expires when browser closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SITE_ID = 1

# If set to False, Django will optimize and not load internationalization.
USE_I18N = False
USE_L10N = False

AUTHENTICATION_BACKENDS = ("mezzanine.core.auth_backends.MezzanineBackend",)

# The numeric mode to set newly-uploaded files to.
# The value should be a mode you'd pass directly to os.chmod.
FILE_UPLOAD_PERMISSIONS = 0o644

#############
# DATABASES #
#############
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.",
        "NAME": "",
        "USER": "",
        "PASSWORD": "",
        # Set to empty string for localhost.
        "HOST": "",
        "PORT": "",
    }
}

#########
# PATHS #
#########

# Full filesystem path to the project.
PROJECT_APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_APP = os.path.basename(PROJECT_APP_PATH)
PROJECT_ROOT = BASE_DIR = os.path.dirname(PROJECT_APP_PATH)

# Every cache key will get prefixed with this value
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_APP

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))
MEDIA_URL = STATIC_URL + "media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))
ROOT_URLCONF = "%s.urls" % PROJECT_APP
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, "templates"),)

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.postgres",
    "django.contrib.humanize",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
    "mezzanine.pages",
    "mezzanine.blog",
    "mezzanine.forms",
    "mezzanine.galleries",
    "mezzanine.twitter",
    "mezzanine.accounts",
    "josstaff",
    "josmembers",
    'request',
    'tracking',
    'django_messages',
    "mailer",
    "ckeditor",
    "cloudinary",
    "pybb",
    # "color_liker",
    # "mezzanine.mobile",
    "josdjoingo",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.static",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.tz",
    "mezzanine.conf.context_processors.settings",
    "mezzanine.pages.context_processors.page",
    "pybb.context_processors.processor",
    'django_messages.context_processors.inbox',

)

# Middleware. Order is important; request classes will be applied in order, response in reverse order.
MIDDLEWARE_CLASSES = (
    "mezzanine.core.middleware.UpdateCacheMiddleware",
    'tracking.middleware.VisitorTrackingMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Uncomment if using internationalisation or localisation
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',

    "mezzanine.core.request.CurrentRequestMiddleware",
    "mezzanine.core.middleware.RedirectFallbackMiddleware",
    "mezzanine.core.middleware.TemplateForDeviceMiddleware",
    "mezzanine.core.middleware.TemplateForHostMiddleware",
    "mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware",
    "mezzanine.core.middleware.SitePermissionMiddleware",
    # Uncomment the following if using any of the SSL settings:
    # "mezzanine.core.middleware.SSLRedirectMiddleware",
    "mezzanine.pages.middleware.PageMiddleware",
    "mezzanine.core.middleware.FetchFromCacheMiddleware",
    'pybb.middleware.PybbMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'request.middleware.RequestMiddleware',
)

# Store these package names here as they may change in the future.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"

#########################
# OPTIONAL APPLICATIONS #

OPTIONAL_APPS = (
    "debug_toolbar",
    "django_extensions",
    "compressor",
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)

########################
# DJANGO DEBUG TOOLBAR #
########################
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

#########
# EMAIL #
#########
# EMAIL_SUBJECT_PREFIX = 'Join Our Story'
# SERVER_EMAIL = EMAIL_HOST_USER = 'joinus@joinourstory.com'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_PASSWORD = '4Primetime!'
# EMAIL_PORT = 587
EMAIL_BACKEND = "mailer.backend.DbBackend"
DEFAULT_FROM_EMAIL = "joinus@joinourstory.com"

###########
# PROFILE #
###########
ACCOUNTS_NO_USERNAME = True
ACCOUNTS_PROFILE_VIEWS_ENABLED = True
AUTH_PROFILE_MODULE = "josmembers.JOSProfile"
ACCOUNTS_PROFILE_FORM_CLASS = "josmembers.forms.JOSProfileForm"
# ACCOUNTS_VERIFICATION_REQUIRED = False
# ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS = ()

############
# CKEDITOR #
############
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_JOSSimpleToolbarConfig': [
            ### {'name': 'document', 'items': ['Preview', 'Print', '-', 'Templates']},
            {'name': 'styles', 'items': ['Font', 'FontSize']},
            {'name': 'clipboard', 'items': ['Undo', 'Redo', 'Cut', 'Copy', 'Paste']},
            ### {'name': 'insert', 'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            ### '/',  # put this to force next toolbar on new line
            {'name': 'basicstyles', 'items': ['Bold', 'Italic', 'Underline', 'Strike']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            ### {'name': 'smiley', 'items': ['Smiley']},
            {'name': 'paragraph', 'items': ['NumberedList', 'BulletedList',
                                            '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight']},
            {'name': 'editing', 'items': ['Find']},
        ],
        'contentsCss': ['/static/ckeditor/ckeditor/contents.css'],
        'toolbar': 'JOSSimpleToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        'height': 600,
        'width': 920,
        'disableNativeSpellChecker': False,
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'removePlugins': 'elementspath, liststyle,tabletools,scayt,menubutton,contextmenu',
        'extraPlugins': ','.join(
            [
                # you extra plugins here
            ]),
    }
}

##############################
# DJANGO- TRACKER & REQUEST  #
##############################
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
# LOCAL SETTINGS #
##################
# Instead of doing "from .local_settings import *", we use exec for full access
f = os.path.join(PROJECT_APP_PATH, "local_settings.py")
if os.path.exists(f):
    exec (open(f, "rb").read())

####################
# DYNAMIC SETTINGS #
####################
# set_dynamic_settings() rewrites globals based on above to provide some better defaults.
try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())
