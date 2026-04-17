from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class InscriptionSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['prenom', 'nom', 'email', 'whatsapp', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Les mots de passe ne correspondent pas."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user


class ConnexionSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ProfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', 'prenom', 'nom', 'email', 'whatsapp',
            'facebook', 'instagram', 'photo_profil',
            'role', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'email', 'role', 'is_active', 'created_at']


class ModifierProfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['prenom', 'nom', 'whatsapp', 'facebook', 'instagram', 'photo_profil']