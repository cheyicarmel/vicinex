import uuid
from django.db import models
from django.conf import settings


class Annonce(models.Model):

    TYPE_LOGEMENT_CHOICES = [
        ('chambre_appart', 'Chambre en appartement'),
        ('chambre_maison', 'Chambre en maison'),
        ('appart_partage', 'Appartement partagé'),
        ('studio_partage', 'Studio partagé'),
    ]

    GENRE_CHOICES = [
        ('mixte', 'Mixte'),
        ('femmes', 'Femmes uniquement'),
        ('hommes', 'Hommes uniquement'),
    ]

    FUMEUR_CHOICES = [
        ('oui', 'Oui'),
        ('non', 'Non'),
        ('indifferent', 'Indifférent'),
    ]

    STATUT_CHOICES = [
        ('etudiant', 'Étudiant'),
        ('actif', 'Actif'),
        ('indifferent', 'Indifférent'),
    ]

    STATUT_ANNONCE_CHOICES = [
        ('publiee', 'Publiée'),
        ('desactivee', 'Désactivée'),
        ('coloc_trouvee', 'Coloc trouvée'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='annonces'
    )
    titre = models.CharField(max_length=255)
    description = models.TextField()
    ville = models.CharField(max_length=100)
    quartier = models.CharField(max_length=100)
    adresse_approx = models.CharField(max_length=255, blank=True, default='')
    type_logement = models.CharField(max_length=20, choices=TYPE_LOGEMENT_CHOICES)
    nb_chambres_total = models.PositiveIntegerField()
    nb_chambres_dispo = models.PositiveIntegerField()
    loyer = models.PositiveIntegerField()
    charges_incluses = models.BooleanField(default=False)
    charges_montant = models.PositiveIntegerField(null=True, blank=True)
    equipements = models.JSONField(default=list)
    pref_genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='mixte')
    pref_fumeur = models.CharField(max_length=20, choices=FUMEUR_CHOICES, default='indifferent')
    pref_statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='indifferent')
    date_dispo = models.DateField()
    latitude = models.DecimalField(max_digits=6, decimal_places=3)
    longitude = models.DecimalField(max_digits=6, decimal_places=3)
    statut = models.CharField(max_length=20, choices=STATUT_ANNONCE_CHOICES, default='publiee')
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Annonce'
        verbose_name_plural = 'Annonces'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.titre} — {self.ville} ({self.user})"


class PhotoAnnonce(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    annonce = models.ForeignKey(
        Annonce,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    url_cloudinary = models.URLField()
    ordre = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
        ordering = ['ordre']

    def __str__(self):
        return f"Photo {self.ordre} — {self.annonce.titre}"


class Signalement(models.Model):

    MOTIF_CHOICES = [
        ('contenu_inapproprie', 'Contenu inapproprié'),
        ('arnaque', 'Arnaque suspectée'),
        ('fausse_annonce', 'Fausse annonce'),
        ('doublon', 'Annonce en doublon'),
        ('autre', 'Autre'),
    ]

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('traite', 'Traité'),
        ('rejete', 'Rejeté'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    annonce = models.ForeignKey(
        Annonce,
        on_delete=models.CASCADE,
        related_name='signalements'
    )
    motif = models.CharField(max_length=30, choices=MOTIF_CHOICES)
    description = models.TextField(blank=True, default='')
    ip_signalant = models.GenericIPAddressField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    decision = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Signalement'
        verbose_name_plural = 'Signalements'
        ordering = ['-created_at']

    def __str__(self):
        return f"Signalement {self.motif} — {self.annonce.titre}"