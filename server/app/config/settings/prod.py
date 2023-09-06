from .base import *

DEBUG = False

ALLOWED_HOSTS = ["uni-bo.net", "www.uni-bo.net"]

STATIC_URL = "static/"
STATIC_ROOT = "/usr/share/nginx/html/static"  # 静的ファイルを集める場所（STATIC_ROOT）を指定

MEDIA_URL = "media/"
MEDIA_ROOT = "/usr/share/nginx/html/media"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_PORT = 25
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = "elephant@uni-bo.net"

DATABASES = {
    "default": env.db(),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
