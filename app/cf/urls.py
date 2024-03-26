from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("assets/", include("assets.urls")),
    path("", include("pwa.urls")),
    path("", include("tickets.urls")),
    path("clients/", include("clients.urls")),
    path("accounts/", include("allauth.urls")),
    path("users/", include("users.urls")),
    path("stickers/", include("stickers.urls")),
    path("cards/", include("cards.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
