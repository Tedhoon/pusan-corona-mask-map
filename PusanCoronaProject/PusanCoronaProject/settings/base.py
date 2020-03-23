import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_SECRET_DIR = os.path.join(BASE_DIR, '.config_secret')
CONFIG_SECRET_BASE_FILE = os.path.join(CONFIG_SECRET_DIR, 'settings_base.json')
CONFIG_SECRET_DEVELOP_FILE = os.path.join(CONFIG_SECRET_DIR, 'settings_develop.json')
CONFIG_SECRET_DEPLOY_FILE = os.path.join(CONFIG_SECRET_DIR, 'settings_deploy.json')
config_secret_base = json.loads(open(CONFIG_SECRET_BASE_FILE).read())
SECRET_KEY = config_secret_base['django']['secret_key']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'src',
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

ROOT_URLCONF = 'PusanCoronaProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'PusanCoronaProject.wsgi.application'


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


# Internationalization

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# 배포시 10분에 한번씩 아래의 함수를 실행하여 데이터베이스를 자동으로 업데이트 합니다.
# 데이터베이스에 환자 동선 정보가 업데이트 되었을 경우 아래에 설정한 이메일로 경보 알람이 갑니다.
CRONJOBS = [
    ('*/10 * * * *', 'main.views.get_mask_stores', '>> /home/ubuntu/mask_stores.log'),
    ('*/10 * * * *', 'main.views.get_status', '>> /home/ubuntu/statistics.log'),
    ('*/10 * * * *', 'main.views.get_patients', '>> /home/ubuntu/patients_crawl.log'),
]

# 경보 메일을 받기 위한 이메일 설정입니다.
# 사용할 이메일의 SMTP 서버 사용을 허용하고 추가하셔야 합니다. 아래 링크는 Gmail 사용 기준 SMTP 서버 사용 가이드입니다.
# https://velog.io/@ground4ekd/django-send-mail#gmail-smtp-%EC%84%9C%EB%B2%84
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = '경보 메일을 받을 이메일 입력'
EMAIL_HOST_PASSWORD = '이메일 비밀번호 입력'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER