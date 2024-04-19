from django.db import models
from django.urls import reverse


class KnowledgeBaseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Knowledge Base Categories"

    def __str__(self):
        return self.name


class KnowledgeBase(models.Model):
    category = models.ForeignKey(
        KnowledgeBaseCategory, on_delete=models.CASCADE, blank=True, null=True
    )
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    attachment = models.FileField(
        upload_to="attachments/knowledgebase/", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("knowledgebase-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class KnowledgeBaseComment(models.Model):
    knowledgebase = models.ForeignKey(KnowledgeBase, on_delete=models.CASCADE)
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comments
