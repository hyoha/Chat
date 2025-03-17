import os
from pathlib import Path

# BASE_DIR: 프로젝트 루트 경로
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key'
DEBUG = True  # 개발 환경에서는 True 유지

ALLOWED_HOSTS = ['*']  # 개발 환경에서는 제한 없음

# 앱 등록 (blog 앱 포함)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'blog',  # blog 앱 등록
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS 미들웨어 추가 (맨 위쪽에 위치 권장)
    # 기존 미들웨어...
    'django.middleware.common.CommonMiddleware',
    # 기타 미들웨어...
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]



ROOT_URLCONF = 'myproject.urls'

CORS_ALLOW_ALL_ORIGINS = True

# 템플릿 설정 (DIRS에 프로젝트 전역 템플릿 폴더 지정)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# 데이터베이스 (SQLite 예시)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 정적 파일 설정
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "blog" / "static"]
