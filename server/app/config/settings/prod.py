from .base import *

DEBUG = False

ALLOWED_HOSTS = ["160.251.10.52"]

STATIC_URL = "static/"
STATIC_ROOT = "/usr/share/nginx/html/static"  # 静的ファイルを集める場所（STATIC_ROOT）を指定

MEDIA_URL = "media/"
MEDIA_ROOT = "/usr/share/nginx/html/media"

DATABASES = {
    "default": env.db(),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
