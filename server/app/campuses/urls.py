from django.urls import path
from .views import (
    UniversityDetailView,
    UniversityListView,
    CampusDetailView,
    CampusListView,
)

urlpatterns = [
    path("university/<uuid:pk>/", UniversityDetailView.as_view(), name="university-detail"),
    path("university/", UniversityListView.as_view(), name="university-list"),
    path("campus/<uuid:pk>/", CampusDetailView.as_view(), name="campus-detail"),
    path("campus/", CampusListView.as_view(), name="campus-list"),
]
