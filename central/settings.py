"""
Configurações do Django para o projeto central.

Gerado por 'django-admin startproject' usando Django 5.0.2.

Para obter mais informações sobre este arquivo, consulte
https://docs.djangoproject.com/en/5.0/topics/settings/

Para a lista completa de configurações e seus valores, consulte
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Construa caminhos dentro do projeto como este: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Configurações rápidas de desenvolvimento - inadequadas para produção
# Consulte https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# AVISO DE SEGURANÇA: mantenha a chave secreta usada em produção em segredo!
SECRET_KEY = 'django-insecure-rk*je+1fb0@%s-0n-(9-=3i&n!7#zdxpoq2x+3)e!i#8wf90oo'

# AVISO DE SEGURANÇA: não execute com debug ativado em produção!
DEBUG = True

ALLOWED_HOSTS = [
    'tcare-central.onrender.com', '*'
]


# Definição de Aplicações

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
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

ROOT_URLCONF = 'central.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'base_templates', #DEFINE A PASTA DE TEMPLATES
        ],
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

WSGI_APPLICATION = 'central.wsgi.application'


# Banco de Dados
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'base_tcare',
        'USER': 'usuario_tcare',
        'PASSWORD': 'VTaQSQgotVjmfyI2g5FUwaCRlbxo9PU6',
        'HOST': 'dpg-codf4520si5c738vjo2g-a.oregon-postgres.render.com',
        'PORT': '5432',
    }
}


# Validação de Senha
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internacionalização
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Boa_Vista'

USE_I18N = True

USE_TZ = True


# Arquivos Estáticos (CSS, JavaScript, Imagens)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    BASE_DIR / 'base_static' ,
) #define os diretórios onde o Django procurará por arquivos estáticos, como arquivos CSS, JavaScript, imagens, etc.

STATIC_ROOT = BASE_DIR / 'static'  # Diretório onde os arquivos estáticos são coletados
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'



MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Tipo de Campo de Chave Primária Padrão
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#importa configurações locais
try:
    from central.local_settings import *
except ImportError:
    ...
