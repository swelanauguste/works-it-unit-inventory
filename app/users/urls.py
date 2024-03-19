from django.urls import path

from .views import ProfileUpdateView, UserUpdateView

urlpatterns = [
    path("user/update/<int:pk>/", UserUpdateView.as_view(), name="user-update"),
    path(
        "profile/update/<slug:slug>/",
        ProfileUpdateView.as_view(),
        name="profile-update",
    ),
]
