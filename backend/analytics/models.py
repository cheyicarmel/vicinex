import uuid
from django.db import models


class PageView(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    path = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    user_agent = models.TextField()
    referer = models.URLField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vue de page'
        verbose_name_plural = 'Vues de pages'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.path} — {self.ip} — {self.created_at}"