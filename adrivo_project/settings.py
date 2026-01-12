from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-clave-secreta-adrivo-final'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'jazzmin',                 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inventario',            
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'adrivo_project.urls'

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
                'inventario.context_processors.alertas_stock',
                'inventario.context_processors.contador_carrito',
            ],
        },
    },
]

WSGI_APPLICATION = 'adrivo_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'adrivoweb_db',
        'USER': 'postgres',
        'PASSWORD': 'adrivo',  
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'OPTIONS': {
            'client_encoding': 'UTF8', 
        }
    }
}

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
]

LANGUAGE_CODE = 'es-ec'
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [BASE_DIR / "static"]

JAZZMIN_SETTINGS = {
    "site_title": "Adrivo Admin",
    "site_header": "Adrivo R.",
    "site_brand": "Adrivo R. Variedades",
    "welcome_sign": "Bienvenida al Universo Adrivo",
    "copyright": "Adrivo R.",
    "site_logo": "logo_adrivo.jpg",
    "login_logo": "logo_adrivo.jpg",
    "site_logo_classes": "img-circle",
    "custom_css": "custom_admin.css",

    "topmenu_links": [
        {"name": "Inicio",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Ver Tienda Web", "url": "home", "icon": "fas fa-store", "new_window": True},
        {"model": "inventario.Producto"},
        {"model": "inventario.Categoria"},
    ],

    "show_ui_builder": False,
    "custom_css": "custom_admin.css",
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "inventario.Producto": "fas fa-shopping-bag", 
        "inventario.Categoria": "fas fa-tags",       
    },
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = '/'
