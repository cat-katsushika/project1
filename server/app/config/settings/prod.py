import os
from datetime import timedelta
from pathlib import Path

import environ
from firebase_admin import initialize_app

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

DEBUG = False

SECRET_KEY = env("SECRET_KEY")

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    "rest_framework",
    "django_filters",
    "rest_framework.authtoken",
    "djoser",
    "corsheaders",
    "fcm_django",
    # Original apps
    "accounts",
    "campuses",
    "comments",
    "items",
    "notifications",
    "terms_and_conditions",
    "transaction_messages",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": env.db(),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "ja"
TIME_ZONE = "Asia/Tokyo"
USE_I18N = True
USE_TZ = True

ALLOWED_HOSTS = ["uni-bo.net", "www.uni-bo.net"]

STATIC_URL = "static/"
STATIC_ROOT = "/usr/share/nginx/html/static"  # 静的ファイルを集める場所（STATIC_ROOT）を指定

MEDIA_URL = "media/"
MEDIA_ROOT = "/usr/share/nginx/html/media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.User"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "accounts.authentication.CookieJWTAuthentication",
    ],
    "DEFAULT_MAX_FILE_SIZE": 10 * 1024 * 1024,  # 最大ファイルサイズ (10MB)
}

CLIENT_URL = env("CLIENT_URL")
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True  # どのリクエストでも許可
    CORS_ALLOW_CREDENTIALS = True  # Cookieの送信の許可
else:
    CORS_ORIGIN_WHITELIST = [CLIENT_URL]  # ホワイトリストに設定したCLIENT_URL（今回はNode.js）のみリクエストを許可
    CORS_ALLOWED_ORIGINS = [CLIENT_URL]
# CSRFトークンの設定
CSRF_TRUSTED_ORIGINS = [CLIENT_URL]

# CORS(クロスドメインリクエスト)でCookieを送信することを許可
CORS_ALLOW_CREDENTIALS = True
# HTTPSの設定とクロスドメインの許可設定
if DEBUG:
    SESSION_COOKIE_SECURE = False
else:
    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = True

SIMPLE_JWT = {
    # アクセストークン(1時間)
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    # リフレッシュトークン(3日)
    "REFRESH_TOKEN_LIFETIME": timedelta(days=3),
    # 認証タイプ
    "AUTH_HEADER_TYPES": ("JWT",),
    # 認証トークン
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_PORT = 25
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = "elephant@uni-bo.net"


DJOSER = {
    # メールアドレスでログイン
    "LOGIN_FIELD": "email",
    # アカウント本登録メール
    "SEND_ACTIVATION_EMAIL": True,
    # アカウント本登録完了メール
    "SEND_CONFIRMATION_EMAIL": True,
    # メールアドレス変更完了メール
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": True,
    # パスワード変更完了メール
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    # アカウント登録時に確認用パスワード必須
    "USER_CREATE_PASSWORD_RETYPE": True,
    # メールアドレス変更時に確認用メールアドレス必須
    "SET_USERNAME_RETYPE": True,
    # パスワード変更時に確認用パスワード必須
    "SET_PASSWORD_RETYPE": True,
    # アカウント本登録用URL
    "ACTIVATION_URL": "/user/activate/{uid}/{token}/",
    # メールアドレスリセット完了用URL
    "USERNAME_RESET_CONFIRM_URL": "email/reset/confirm/{uid}/{token}/",
    # パスワードリセット完了用URL
    "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}/",
    # カスタムユーザー用シリアライザー
    "SERIALIZERS": {
        "user_create": "accounts.serializers.UserSerializer",
        "user_create_password_retype": "accounts.serializers.UserCreateSerializer",
        "user": "accounts.serializers.UserSerializer",
        "current_user": "accounts.serializers.UserSerializer",
    },
    "PERMISSIONS": {
        "user": ["djoser.permissions.CurrentUserOrAdminOrReadOnly"],
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

# FCM関連
FIREBASE_APP = initialize_app()
