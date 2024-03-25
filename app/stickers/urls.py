from django.urls import path

from .views import (
    StickerClerkListView,
    StickerCreateView,
    StickerDetailView,
    StickerUpdateView,
)

urlpatterns = [
    path("clerk-stickers/", StickerClerkListView.as_view(), name="sticker-clerk-list"),
    path("stickers/create/", StickerCreateView.as_view(), name="sticker-create"),
    path("stickers/<int:pk>/", StickerDetailView.as_view(), name="sticker-detail"),
    path(
        "stickers/<int:pk>/update/", StickerUpdateView.as_view(), name="sticker-update"
    ),
]
