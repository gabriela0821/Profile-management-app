"""
Serializers para la API de usuarios y perfiles.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    """Serializer para el modelo User de Django"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username']


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Profile"""
    
    user = UserSerializer(read_only=True)
    foto_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'telefono',
            'documento', 
            'tipo_usuario',
            'tipo_naturaleza',
            'biografia',
            'foto',
            'foto_url',
            'linkedin',
            'twitter',
            'github',
            'sitio_web',
            'esta_verificado',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'foto_url']
    
    def get_foto_url(self, obj):
        """Obtener URL completa de la foto"""
        if obj.foto:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto.url)
            return obj.foto.url
        return None


class ProfileUpdateSerializer(serializers.Serializer):
    """Serializer para actualizar perfil completo (usuario + profile)"""
    
    user = serializers.DictField()
    telefono = serializers.CharField(max_length=15, required=False, allow_blank=True)
    documento = serializers.CharField(max_length=20, required=False, allow_blank=True)
    tipo_usuario = serializers.ChoiceField(
        choices=Profile.TIPO_USUARIO_CHOICES,
        required=False
    )
    tipo_naturaleza = serializers.ChoiceField(
        choices=Profile.TIPO_NATURALEZA_CHOICES,
        required=False
    )
    biografia = serializers.CharField(max_length=500, required=False, allow_blank=True)
    linkedin = serializers.URLField(required=False, allow_blank=True)
    twitter = serializers.URLField(required=False, allow_blank=True)
    github = serializers.URLField(required=False, allow_blank=True)
    sitio_web = serializers.URLField(required=False, allow_blank=True)
    esta_verificado = serializers.CharField(required=False)  # Viene como string del frontend
    
    def validate_user(self, value):
        """Validar datos del usuario"""
        required_fields = ['first_name', 'last_name']
        for field in required_fields:
            if field not in value or not value[field].strip():
                raise serializers.ValidationError(f'{field} is required')
        return value
    
    def validate_esta_verificado(self, value):
        """Convertir string a boolean"""
        if isinstance(value, str):
            return value.lower() in ['true', '1', 'yes', 'on']
        return bool(value)
    
    def update_profile(self, user, validated_data):
        """Actualizar perfil y usuario"""
        # Actualizar datos del usuario
        user_data = validated_data.pop('user', {})
        if user_data:
            for field, value in user_data.items():
                setattr(user, field, value)
            user.save()
        
        # Actualizar perfil
        profile = user.profile
        for field, value in validated_data.items():
            if field == 'esta_verificado':
                # Convertir string a boolean
                if isinstance(value, str):
                    value = value.lower() in ['true', '1', 'yes', 'on']
            
            # Limpiar campos vacíos para URLs
            if field in ['linkedin', 'twitter', 'github', 'sitio_web']:
                if value == '':
                    value = None
            
            setattr(profile, field, value)
        
        profile.save()
        return profile


class PhotoUploadSerializer(serializers.Serializer):
    """Serializer para subida de fotos de perfil"""
    
    foto = serializers.ImageField()
    
    def validate_foto(self, value):
        """Validar archivo de imagen"""
        # Validar tamaño (máximo 5MB)
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("La imagen es muy grande. Máximo 5MB permitido.")
        
        # Validar tipo de archivo
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("Tipo de archivo no permitido. Use JPG, PNG o GIF.")
        
        return value


class LoginResponseSerializer(serializers.Serializer):
    """Serializer para respuesta de login"""
    
    access = serializers.CharField()
    refresh = serializers.CharField()
    
    
class ApiResponseSerializer(serializers.Serializer):
    """Serializer para respuestas estándar de la API"""
    
    status = serializers.ChoiceField(choices=['success', 'error'])
    message = serializers.CharField()
    data = serializers.JSONField(required=False)