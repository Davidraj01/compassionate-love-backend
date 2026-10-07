"""
Django settings for clm_backend project.
Compassionate Love of Calvary Ministries Backend.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env with explicit path and override=True
load_dotenv(BASE_DIR / '.env', override=True)


# SECURITY: Secret key from environment variable with safe fallback for dev
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-clm-calvary-ministries-secret-key-2026-prod-grade')

# DEBUG mode - set to False in production
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    
    # Local apps
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'clm_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'clm_backend.wsgi.application'

# Database Configuration (MySQL / SQL / SQLite fallback)
# Defaults to SQLite for immediate zero-config plug-and-play, supports MySQL via environment variables.
DB_ENGINE = os.environ.get('DB_ENGINE', 'sqlite')
if DB_ENGINE == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', 'clm_db'),
            'USER': os.environ.get('DB_USER', 'root'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
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

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS = True  # For seamless local development with Vite
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://localhost:\d+$",
    r"^http://127.0.0.1:\d+$",
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static and Media files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# ============================================================================
# RAZORPAY & MINISTRY OWNER FINANCIAL CONFIGURATION
# ============================================================================
# Secure Razorpay payment gateway credentials
RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', 'rzp_test_clmDemoKey123')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', 'clmDemoSecretKey456')
RAZORPAY_CURRENCY = 'INR'

# Ministry Owner Financial & Bank Account details for Direct Transfer & UPI Scanner
MINISTRY_OWNER_EMAIL = os.environ.get('MINISTRY_OWNER_EMAIL', 'davidraj2107@gmail.com')
MINISTRY_OWNER_PHONE = os.environ.get('MINISTRY_OWNER_PHONE', '+91 9994401291')
MINISTRY_LEGAL_NAME = os.environ.get('MINISTRY_LEGAL_NAME', 'Compassionate Love of Calvary Ministries')
MINISTRY_UPI_ID = os.environ.get('MINISTRY_UPI_ID', 'dr.s.davidraj-1@okicici')
MINISTRY_BANK_NAME = os.environ.get('MINISTRY_BANK_NAME', 'ICICI Bank')

MINISTRY_ACCOUNT_NAME = os.environ.get('MINISTRY_ACCOUNT_NAME', 'Compassionate Love of Calvary Ministries / Pastor David Raj')
MINISTRY_ACCOUNT_NO = os.environ.get('MINISTRY_ACCOUNT_NO', '039801507262')
MINISTRY_IFSC_CODE = os.environ.get('MINISTRY_IFSC_CODE', 'ICIC0000398')
MINISTRY_BRANCH = os.environ.get('MINISTRY_BRANCH', ' Chengalpattu')


# Email Configuration (for automatic instant receipts & owner notifications)
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend' if os.environ.get('EMAIL_HOST_PASSWORD') else 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'davidraj2107@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = f"Compassionate Love of Calvary Ministries <{os.environ.get('DEFAULT_FROM_EMAIL', 'davidraj2107@gmail.com')}>"



