from django.contrib import admin

from .models import KnowledgeBase, KnowledgeBaseCategory, KnowledgeBaseComment

admin.site.register(KnowledgeBase)
admin.site.register(KnowledgeBaseCategory)
admin.site.register(KnowledgeBaseComment)
