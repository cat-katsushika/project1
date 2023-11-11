from django.urls import path

from .views import NotificationView

urlpatterns = [
    path("", NotificationView.as_view(), name="notification-list"),
]
