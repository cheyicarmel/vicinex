import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from .models import User
from .serializers import InscriptionSerializer, ConnexionSerializer, ProfilSerializer, ModifierProfilSerializer


class InscriptionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = InscriptionSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = str(uuid.uuid4())
            user.verification_token = token
            user.save()
            lien = f"http://localhost:8000/api/auth/verification-email/{token}/"
            send_mail(
                subject="Confirmez votre adresse email — Vicinex",
                message=f"Bonjour {user.prenom},\n\nCliquez sur ce lien pour activer votre compte :\n{lien}\n\nCe lien expire dans 24 heures.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return Response(
                {"message": "Compte créé. Vérifiez votre email pour activer votre compte."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerificationEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            user = User.objects.get(verification_token=token)
            if user.email_verified:
                return Response(
                    {"message": "Ce compte est déjà activé."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.is_active = True
            user.email_verified = True
            user.verification_token = ''
            user.save()
            return Response(
                {"message": "Email vérifié. Vous pouvez maintenant vous connecter."},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"message": "Lien invalide ou expiré."},
                status=status.HTTP_400_BAD_REQUEST
            )


class ConnexionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ConnexionSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, username=email, password=password)
            if user is None or not user.is_active or user.is_banned:
                return Response(
                    {"message": "Identifiants incorrects."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": ProfilSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeconnexionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Déconnexion réussie."},
                status=status.HTTP_200_OK
            )
        except TokenError:
            return Response(
                {"message": "Token invalide."},
                status=status.HTTP_400_BAD_REQUEST
            )


class ResetMotDePasseView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            token = str(uuid.uuid4())
            user.reset_token = token
            user.save()
            lien = f"http://localhost:8000/api/auth/mot-de-passe/reset/confirm/?token={token}"
            send_mail(
                subject="Réinitialisation de mot de passe — Vicinex",
                message=f"Bonjour {user.prenom},\n\nCliquez sur ce lien pour réinitialiser votre mot de passe :\n{lien}\n\nCe lien expire dans 1 heure.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except User.DoesNotExist:
            pass
        return Response(
            {"message": "Le lien de réinitialisation a été envoyé à votre adresse email."},
            status=status.HTTP_200_OK
        )


class ResetMotDePasseConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        password = request.data.get('password')
        password2 = request.data.get('password2')
        if not token or not password or not password2:
            return Response(
                {"message": "Données manquantes."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if password != password2:
            return Response(
                {"message": "Les mots de passe ne correspondent pas."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(reset_token=token)
            user.set_password(password)
            user.reset_token = ''
            user.save()
            return Response(
                {"message": "Mot de passe réinitialisé avec succès."},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"message": "Lien invalide ou expiré."},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProfilView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfilSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = ModifierProfilSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(
            {"message": "Compte supprimé avec succès."},
            status=status.HTTP_204_NO_CONTENT
        )