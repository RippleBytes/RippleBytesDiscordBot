"""
Django settings for RippleBytesDiscordBot project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os  
from django.conf import settings
from pathlib import Path
from datetime import timedelta
from decouple import config
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*','https://operation.ripplebytes.com']

CORS_ALLOWED_ORIGINS = [
    "https://operation.ripplebytes.com"
]

CSRF_TRUSTED_ORIGINS = ['https://operation.ripplebytes.com']


# Application definition

INSTALLED_APPS = [
    "unfold", 
    "unfold.contrib.filters",  
    "unfold.contrib.forms", 
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'bot',
    'django_browser_reload',
    'import_export'
    
]
UNFOLD = {
    "SITE_TITLE": "RippleBytes",
    "SITE_HEADER": "RippleBytes",
     "SIDEBAR": {
        "show_search": False,  # Search in applications and models names
        "show_all_applications": False,  # Dropdown with all applications and models
        "navigation": [
            {
                'items':
                [
                    {
                        "title": _("Dashboard"), 
                        "icon": "menu",  
                        "link": reverse_lazy("admin:index"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ]

            },
            {
                "title":_('Users'),
                "separator":True,
                "collapsible":True,
                "items":
                [
                    {
                        "title": _("Users"), 
                        "icon": "person",
                        "link": reverse_lazy("admin:bot_user_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    
                    {
                        "title": _("Groups"), 
                        "icon": "people",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ]
            },
            {
                'title':_('Office bot records'),
                "separator": True,  # Top border
                "collapsible": True,  # Collapsible group of links
                "items": [
                    
                    
                    {
                        "title": _("Bank Details"), 
                        "icon": "savings",
                        "link": reverse_lazy("admin:bot_bankdetail_changelist"),
                    },
                    {
                        "title": _("Break Record"), 
                        "icon": "logout",
                        "link": reverse_lazy("admin:bot_breakrecord_changelist"),
                    },
                    {
                        "title": _("Checkin Record"), 
                        "icon": "check",
                        "link": reverse_lazy("admin:bot_checkinrecord_changelist"),
                    },
                    
                    {
                        "title": _("Leave request"), 
                        "icon": "waving_hand",
                        "link": reverse_lazy("admin:bot_leaverequest_changelist"),
                    },
                    {
                        "title": _("Task_record"), 
                        "icon": "keep",  
                        "link": reverse_lazy("admin:bot_taskrecord_changelist"),
                    },
                    
                ],
            },
        ],
    },
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'RippleBytesDiscordBot.middleware.TimezoneMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = 'RippleBytesDiscordBot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'RippleBytesDiscordBot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB',default='office_bot'),
        'USER': config('POSTGRES_USER',default='postgres'),
        'PASSWORD': config('POSTGRES_PASSWORD',default='password'),
        'HOST': config('POSTGRES_HOST',default='localhost'),
        'PORT': config('POSTGRES_PORT',default=5432),
    }
}

REST_FRAMEWORK={
    
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY":settings.SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_TZ = True

MEDIA_URL='/documents/'
MEDIA_ROOT=BASE_DIR/'documents'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DISCORD_TOKEN=config('DISCORD_TOKEN')
LEAVE_CHANNEL_ID=config('LEAVE_CHANNEL_ID')
ADMIN_CHANNEL_ID=config('ADMIN_CHANNEL_ID')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DISCORD_WEBHOOK_URL=config('DISCORD_WEBHOOK_URL')
REDIRECT_URL=config('REDIRECT_URL')

AUTH_USER_MODEL='bot.User'