from django.urls import path

from .views import (
    KnowledgeBaseCommentCreateView,
    KnowledgeBaseCreateView,
    KnowledgeBaseDetailView,
    KnowledgeBaseListView,
    KnowledgeBaseUpdateView,
)

urlpatterns = [
    path("", KnowledgeBaseListView.as_view(), name="knowledgebase-list"),
    path("detail/<int:pk>/", KnowledgeBaseDetailView.as_view(), name="knowledgebase-detail"),
    path("create/", KnowledgeBaseCreateView.as_view(), name="knowledgebase-create"),
    path("update/<int:pk>/", KnowledgeBaseUpdateView.as_view(), name="knowledgebase-update"),
    path(
        "comment/create/<int:pk>/",
        KnowledgeBaseCommentCreateView.as_view(),
        name="knowledgebase-comment-create",
    ),
]
