from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/", include("campuses.urls")),
    path("api/comment/", include("comments.urls")),
    path("api/items/", include("items.urls")),
    path("api/messages/", include("transaction_messages.urls")),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    path("api/", include("accounts.urls")),
    path("api/auth/", include("djoser.urls.authtoken")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
