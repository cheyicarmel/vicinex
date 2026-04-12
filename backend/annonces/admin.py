from django.contrib import admin
from .models import Annonce, PhotoAnnonce, Signalement


@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ['titre', 'ville', 'quartier', 'loyer', 'statut', 'user', 'created_at']
    list_filter = ['statut', 'ville', 'type_logement', 'pref_genre']
    search_fields = ['titre', 'ville', 'quartier', 'description']
    ordering = ['-created_at']


@admin.register(PhotoAnnonce)
class PhotoAnnonceAdmin(admin.ModelAdmin):
    list_display = ['annonce', 'ordre', 'created_at']
    ordering = ['annonce', 'ordre']


@admin.register(Signalement)
class SignalementAdmin(admin.ModelAdmin):
    list_display = ['annonce', 'motif', 'statut', 'ip_signalant', 'created_at']
    list_filter = ['statut', 'motif']
    ordering = ['-created_at']