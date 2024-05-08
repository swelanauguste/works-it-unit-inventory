from django.urls import path

from .views import (
    CardCreateView,
    CardDetailView,
    CardListView,
    CardUpdateView,
    card_filter_view,
    card_view,
)

urlpatterns = [
    path("card/", CardListView.as_view(), name="card-list"),
    path("card/<int:pk>/", CardDetailView.as_view(), name="card-detail"),
    path("create/", CardCreateView.as_view(), name="card-create"),
    path("create/<int:pk>/", CardUpdateView.as_view(), name="card-update"),
    path("card-filter", card_filter_view, name="card-filter"),
    path("card-view/<int:pk>/", card_view, name="card"),
]
