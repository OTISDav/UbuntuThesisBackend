import os
from pathlib import Path
from decouple import config
import dj_database_url
import cloudinary


# Chemins de construction à l'intérieur du projet comme ceci : BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Paramètres de développement rapides - non adaptés pour la production
SECRET_KEY = config('SECRET_KEY')  # Utiliser la clé secrète à partir de la variable d'environnement
# DEBUG = False  # À changer en False en production
DEBUG = True


ALLOWED_HOSTS = [
    "ubuntuthesisbackend.onrender.com",
    "localhost",
    "127.0.0.1"
]

# Définition des applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_rest_passwordreset',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'drf_yasg',
    'django_filters',
    'cloudinary',
    'cloudinary_storage',
    'users',
    'theses',
    'documents',
    'corsheaders',
    'notifications',
    'push_notifications',

    'django.contrib.sites',  # obligatoire pour allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'thesisfinder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [BASE_DIR / 'templates'],
        # 'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'DIRS': [BASE_DIR / 'users' / 'templates'],
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

WSGI_APPLICATION = 'thesisfinder.wsgi.application'
AUTH_USER_MODEL = 'users.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),  # durée du token d'accès
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # durée du token de refresh
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}


FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": "BP6VFaIC3NMkc_7UlwkN5j6JTwXhZNVOND73ZO2-V0HuN8INi8YotRdf3Msp5m45C3qlRrpn3lc-7lJ0dxjoMpA",
}


CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:54282",
    "http://127.0.0.1:8000"
]

# Configuration de la base de données
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://neondb_owner:npg_1DOG3arBETQv@ep-tiny-breeze-a84c5xue-pooler.eastus2.azure.neon.tech/neondb?sslmode=require',
        conn_max_age=600
    )
}

# Validation des mots de passe
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


DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ddavidotis@gmail.com'          # ton email gmail
EMAIL_HOST_PASSWORD = 'zylj yffd lvni rspu'     # mot de passe d'application (à créer dans Google)
DEFAULT_FROM_EMAIL = 'THESE <ddavidotis@gmail.com>'  # L'adresse d'envoi visible pour les destinataires
SERVER_EMAIL = DEFAULT_FROM_EMAIL





EMAIL_USE_LOCALTIME = True
# LOGGING = {
#     'version': 1,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.mail': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     },
# }


SITE_ID = 1

REST_USE_JWT = True  # si tu utilises JWT

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # backend standard
    'allauth.account.auth_backends.AuthenticationBackend',  # allauth
)

# Configuration allauth
ACCOUNT_EMAIL_VERIFICATION = 'none'  # ou 'mandatory' si tu veux
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True

FRONTEND_URL = "https://ubuntuthesisbackend.onrender.com/api/users/auth"
# https://ubuntuthesisbackend.onrender.com/api/users/auth/activate/

cloudinary.config(
  cloud_name = 'dkk95mjgt',
  api_key = '956771579914482',
  api_secret = 'TX4keeAJMpMDTAPQoySzg4qDnxs',
  secure = True,

)



# Internationalisation
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True



# Type de champ clé primaire par défaut
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuration de Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# Configuration supplémentaire pour les fichiers statiques
# Ne laisse qu'une seule fois cette ligne :
STATIC_URL = '/static/'

# Laisse STATIC_ROOT uniquement si DEBUG=False
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')



