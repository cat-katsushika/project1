from django.urls import path

from . import views

app_name = "items"

urlpatterns = [
    path("", views.ItemListCreateView.as_view()),
    path("<uuid:pk>/", views.ItemRetrieveUpdateDestroyView.as_view()),
    path("<uuid:pk>/purchase/", views.ItemPurchaseView.as_view()),
    path("<uuid:pk>/cancel/", views.ItemCancelView.as_view()),
    path("<uuid:pk>/complete/", views.ItemCompleteView.as_view()),
    path("<uuid:pk>/like-toggle/", views.ItemLikeToggleView.as_view()),
    path("profile/like/", views.LikeItemListView.as_view()),
]
