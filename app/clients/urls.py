from django.urls import path

from .views import (
    ClientCreateView,
    ClientDetailView,
    ClientListView,
    ClientUpdateView,
    DepartmentListView,
)

urlpatterns = [
    path("", ClientListView.as_view(), name="client-list"),
    path("create/", ClientCreateView.as_view(), name="client-create"),
    path("detail/<int:pk>/", ClientDetailView.as_view(), name="client-detail"),
    path("update/<int:pk>/", ClientUpdateView.as_view(), name="client-update"),
    path("departments/", DepartmentListView.as_view(), name="department-list"),
]