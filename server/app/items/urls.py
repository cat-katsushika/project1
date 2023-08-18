from django.urls import path

from . import views

app_name = "items"

urlpatterns = [
    path("", views.ItemListCreateView.as_view()),
    path("<uuid:pk>/", views.ItemRetrieveUpdateDestroyView.as_view()),
]
