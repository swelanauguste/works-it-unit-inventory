from django.urls import path

from .views import (
    CardCreateView,
    CardDetailView,
    CardListView,
    CardUpdateView,
    StaffCardCreateView,
    StaffCardDetailView,
    StaffCardListView,
    StaffCardUpdateView,
    card_filter_view,
    staff_card_view,
)

urlpatterns = [
    path("card/", CardListView.as_view(), name="card-list"),
    path("card/<int:pk>/", CardDetailView.as_view(), name="card-detail"),
    path("create/", CardCreateView.as_view(), name="card-create"),
    path("create/<int:pk>/", CardUpdateView.as_view(), name="card-update"),
    path("card-filter", card_filter_view, name="card-filter"),
    path(
        "staff-card/detail/<int:pk>/",
        StaffCardDetailView.as_view(),
        name="staff-card-detail",
    ),
    path(
        "staff-card/update/<int:pk>/",
        StaffCardUpdateView.as_view(),
        name="staff-card-update",
    ),
    path("staff-card-create/", StaffCardCreateView.as_view(), name="staff-card-create"),
    path("staff-card/", StaffCardListView.as_view(), name="staff-card-list"),
    path("staff-card/<int:pk>/", staff_card_view, name="staff-card-view"),
]
