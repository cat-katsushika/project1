from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("campuses.urls")),
    path("api/comment/", include("comments.urls")),
    path("api/items/", include("items.urls")),
    path("api/messages/", include("transaction_messages.urls")),
    path("api/auth/", include("djoser.urls")),
    path("api/", include("accounts.urls")),
    path("", include("terms_and_conditions.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularRedocView,
        SpectacularSwaggerView,
    )

    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),  # 追加
        path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),  # 追加
        path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),  # 追加
    ]
