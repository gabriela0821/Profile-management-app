"""
Views para la API de usuarios y perfiles.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Profile
from .serializers import (
    ProfileSerializer, 
    ProfileUpdateSerializer, 
    PhotoUploadSerializer,
    LoginResponseSerializer,
    ApiResponseSerializer
)


def get_api_response(status_type, message, data=None):
    """Generar respuesta estándar de la API"""
    response_data = {
        'status': status_type,
        'message': message
    }
    if data is not None:
        response_data['data'] = data
    return response_data


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Endpoint para autenticación de usuario
    POST /usuarios/api/login/
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            get_api_response('error', 'Username y password son requeridos'),
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Autenticar usuario
    user = authenticate(username=username, password=password)
    
    if user is not None:
        if user.is_active:
            # Generar tokens JWT
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            # Respuesta con tokens
            response_data = {
                'access': str(access_token),
                'refresh': str(refresh),
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                get_api_response('error', 'Cuenta desactivada'),
                status=status.HTTP_401_UNAUTHORIZED
            )
    else:
        return Response(
            get_api_response('error', 'Credenciales inválidas'),
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """
    Obtener perfil del usuario autenticado
    GET /usuarios/api/perfil/
    """
    try:
        profile = request.user.profile
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        # Crear perfil si no existe
        profile = Profile.objects.create(user=request.user)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            get_api_response('error', f'Error al obtener perfil: {str(e)}'),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Actualizar perfil completo del usuario
    PUT /usuarios/api/usuario/perfil/
    """
    try:
        with transaction.atomic():
            serializer = ProfileUpdateSerializer(data=request.data)
            
            if serializer.is_valid():
                # Actualizar perfil
                profile = serializer.update_profile(request.user, serializer.validated_data)
                
                # Retornar perfil actualizado
                profile_serializer = ProfileSerializer(profile, context={'request': request})
                
                return Response(
                    get_api_response(
                        'success', 
                        'Perfil actualizado correctamente',
                        profile_serializer.data
                    ),
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    get_api_response('error', 'Datos inválidos', serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST
                )
                
    except Exception as e:
        return Response(
            get_api_response('error', f'Error al actualizar perfil: {str(e)}'),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def upload_profile_photo(request):
    """
    Subir foto de perfil
    PATCH /usuarios/api/perfil/foto/
    """
    try:
        profile = request.user.profile
        serializer = PhotoUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            # Eliminar foto anterior si existe
            if profile.foto:
                profile.foto.delete(save=False)
            
            # Guardar nueva foto
            profile.foto = serializer.validated_data['foto']
            profile.save()
            
            # Retornar respuesta
            profile_serializer = ProfileSerializer(profile, context={'request': request})
            
            return Response(
                get_api_response(
                    'success',
                    'Foto actualizada correctamente',
                    profile_serializer.data
                ),
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                get_api_response('error', 'Archivo inválido', serializer.errors),
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Profile.DoesNotExist:
        return Response(
            get_api_response('error', 'Perfil no encontrado'),
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            get_api_response('error', f'Error al subir foto: {str(e)}'),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_token(request):
    """
    Renovar token de acceso
    POST /usuarios/api/token/refresh/
    """
    try:
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response(
                get_api_response('error', 'Refresh token requerido'),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            
            return Response({
                'access': str(access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)
            
        except Exception:
            return Response(
                get_api_response('error', 'Token inválido'),
                status=status.HTTP_401_UNAUTHORIZED
            )
            
    except Exception as e:
        return Response(
            get_api_response('error', f'Error al renovar token: {str(e)}'),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    """
    Información básica del usuario (para debugging)
    GET /usuarios/api/user/info/
    """
    user_data = {
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'is_active': request.user.is_active,
        'date_joined': request.user.date_joined,
    }
    
    return Response(
        get_api_response('success', 'Información del usuario', user_data),
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    """
    Endpoint para verificar estado de la API
    GET /usuarios/api/status/
    """
    return Response(
        get_api_response(
            'success', 
            'API funcionando correctamente',
            {
                'version': '1.0.0',
                'endpoints': [
                    '/usuarios/api/login/',
                    '/usuarios/api/perfil/',
                    '/usuarios/api/usuario/perfil/',
                    '/usuarios/api/perfil/foto/',
                    '/usuarios/api/token/refresh/',
                ]
            }
        ),
        status=status.HTTP_200_OK
    )