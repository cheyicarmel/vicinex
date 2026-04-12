from django.contrib import admin
from .models import PageView


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['path', 'ip', 'referer', 'created_at']
    search_fields = ['path', 'ip']
    ordering = ['-created_at']