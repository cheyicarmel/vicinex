from django.urls import path
from . import views

urlpatterns = [
    path('inscription/', views.InscriptionView.as_view(), name='inscription'),
    path('verification-email/<str:token>/', views.VerificationEmailView.as_view(), name='verification-email'),
    path('connexion/', views.ConnexionView.as_view(), name='connexion'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token-refresh'),
    path('deconnexion/', views.DeconnexionView.as_view(), name='deconnexion'),
    path('mot-de-passe/reset/', views.ResetMotDePasseView.as_view(), name='reset-mdp'),
    path('mot-de-passe/reset/confirm/', views.ResetMotDePasseConfirmView.as_view(), name='reset-mdp-confirm'),
    path('profil/', views.ProfilView.as_view(), name='profil'),
]