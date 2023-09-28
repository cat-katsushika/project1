# from django.urls import path

from django.urls import path

from .views import (
    JWTokenObtainView,
    JWTokenRefreshView,
    LogoutView,
    UserListAPIView,
    user_activation_view,
)

urlpatterns = [
    path("users/", UserListAPIView.as_view()),
    path("auth/jwt/create/", JWTokenObtainView.as_view()),
    path("auth/jwt/refresh/", JWTokenRefreshView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
    path("auth/user/activate/<str:uid>/<str:token>/", user_activation_view),
]
