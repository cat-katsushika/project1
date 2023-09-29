# from django.urls import path

from django.urls import path

from .views import (
    JWTokenObtainView,
    JWTokenRefreshView,
    LogoutView,
    UserListAPIView,
    user_activate_view,
)

urlpatterns = [
    path("users/", UserListAPIView.as_view()),
    path("auth/jwt/create/", JWTokenObtainView.as_view(), name="login"),
    path("auth/jwt/refresh/", JWTokenRefreshView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
    path("user/activate/<str:uid>/<str:token>/", user_activate_view),
]
