"""
Django settings for secret_storage project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from secret_storage.shortcuts.bower_finder import BowerFinder, replace_conf
from secret_storage.shortcuts.views_rest import ApiRouter

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
join = lambda *path: os.path.abspath(os.path.join(*path))
PROJECT_PATH = join(os.path.dirname(__file__))
ROOT_PATH = join(PROJECT_PATH, '../..')
PUBLIC_PATH = join(ROOT_PATH, 'public')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # default
    'guardian.backends.ObjectPermissionBackend',
)

ANONYMOUS_USER_ID = -1
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'security',
    'guardian',
    'django_evolution',
    'secret_storage',
    'rest_framework',
    'pipeline',
    # 'rest_framework.authtoken',
    'djangobower',
    'office_manager',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'security.middleware.ContentSecurityPolicyMiddleware',
    'security.middleware.DoNotTrackMiddleware',
    'security.middleware.ContentNoSniff',
    'security.middleware.XssProtectMiddleware',
)

ROOT_URLCONF = 'secret_storage.urls'

WSGI_APPLICATION = 'secret_storage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        'ENGINE': 'demo.db',
        'NAME': join(BASE_DIR, 'db.sqlite3'),
        'DEMO_PATH': join(ROOT_PATH, 'demo_dbs'),
        'DEMO_DB': join(BASE_DIR, 'demo.sqlite3')
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = join(PUBLIC_PATH, 'static')
TEMP_ROOT = join(ROOT_PATH, 'temp')
TEMPORARY_STORAGE = 'secret_storage.storage.TempStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
    'djangular.finders.NamespacedAngularAppDirectoriesFinder',
)
STATICFILES_STORAGE = 'secret_storage.storage.PublicCachedStorage'
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'
PIPELINE_YUI_BINARY = 'java -jar ../tools/yuicompressor-2.4.8.jar'
# PIPELINE_JS_COMPRESSOR=None
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.closure.ClosureCompressor'
PIPELINE_CLOSURE_BINARY = r'java -jar ../tools/compiler.jar'
PIPELINE_NGMIN_BINARY = r'C:\Users\Maxaon\AppData\Roaming\npm\ngmin.cmd'

BOWER_COMPONENTS_ROOT = join(ROOT_PATH)
BOWER_INSTALLED_APPS = {
    'angular#1.2.16': {
        'dependencies': ['jquery']
    },
    'angular-bootstrap#0.11.0': None,
    'angular-cookies#1.2.16': None,
    'angular-gravatar#0.1.4': None,
    'angular-sanitize#1.2.16': None,
    'angular-ui-router': None,
    'bootstrap#3.1.1': None,
    'fontawesome#4.1.0': None,
    'https://github.com/maxaon/ng-table.git#b3b759192842b8c46fa341db6361ddcb43686f11': None,
    'https://github.com/maxaon/sun-angular-diff.git#b2d58d4ce0adcb4626a1625d0d0179414dd283a7': None,
    'https://github.com/maxaon/sun-rest.git#89ca41fd33ae23a2d9786b70869250dae559e479': None,
    'https://github.com/maxaon/ui-router.git#1a77d677f978e4596b0a0d64fe48fea6c97c41fe': None,
    'ionicons#1.4.1': None,
    'jquery#2.1.1': None,
    'jquery-migrate#1.2.1': {
        'dependencies': ['jquery'],
        'main': 'jquery-migrate.js',
        'name': 'jquery-migrate'
    },
    'lodash#2.4.1': 'dist/lodash.js',
}

bower_finder = BowerFinder(join(BOWER_COMPONENTS_ROOT, 'bower_components'), BOWER_INSTALLED_APPS)
PIPELINE_CSS = {
    'bower': {
        'source_filenames': bower_finder.get('.css') + [
            'angular/angular-csp.css',
            'theme/admin-lte.css'
        ],
        'output_filename': 'bower.css'
    }
}

PIPELINE_JS = {
    'bower': {
        'source_filenames': [
                                'errorCatch.js'
                            ]
                            +
                            bower_finder.get('.js')
                            +
                            [
                                'vendor/*.js',
                                'openpgp.js',
                                'theme/admin-lte.js',
                                'templateCache.js',
                                'sun-angular-diff/**/*.js',
                            ],
        'output_filename': 'bower.js'
    },
    'app': {
        'source_filenames': [
            'app/secret_storage/**/*.js',
            'app/office_manager/**/*.js'
        ],
        'output_filename': 'app.js'
    },
    'openpgp': {
        'source_filenames': [
            'openpgp.js',
        ],
        'output_filename': 'openpgp.js'
    },
    'openpgpwork': {
        'source_filenames': [
            'openpgp.worker.js'
        ],
        'output_filename': 'openpgp.worker.js'
    }

}

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoObjectPermissions'
    ]
}

CSP_MODE = 'report-only'
CSP_DICT = {
    'default-src': ['self'],
    'script-src': ['self'],
    'style-src': ['self'],
    'img-src': ['self', 'http://www.gravatar.com'],
    'connect-src': ['self'],
    'font-src': ['self'],
    'object-src': ['none'],
    'media-src': ['none'],
    'frame-src': ['none'],
    # 'sandbox': [''],
    # report URI is *not* array
    'report-uri': '/csp-report',
}

API_ROUTER = ApiRouter('secret_storage.routes.MyMegaRouter', trailing_slash=False)
API_ROUTER.trailing_slash = "/?"

try:
    from  secret_storage.settings_personal import *
except ImportError:
    pass

if not DEBUG or os.environ.get("COLLECT_STATIC", False):
    PIPELINE_COMPILERS = (
        'pipeline.compilers.ngmin.NgMinCompiler',
    )
    replace_conf(PIPELINE_JS, 'bower', 'angular.js', 'angular.min.js', )
    replace_conf(PIPELINE_JS, 'bower', 'lodash.js', 'lodash.min.js', )

