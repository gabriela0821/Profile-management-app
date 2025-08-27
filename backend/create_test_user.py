#!/usr/bin/env python
"""
Script para crear usuario de prueba para la prueba técnica
Ejecutar con: python manage.py shell < create_test_user.py
"""

from django.contrib.auth.models import User
from usuarios.models import Profile

# Crear usuario de prueba
username = 'carlosandresmoreno'
password = '90122856_Hanz'

# Verificar si el usuario ya existe
if User.objects.filter(username=username).exists():
    print(f"Usuario {username} ya existe")
    user = User.objects.get(username=username)
else:
    # Crear usuario
    user = User.objects.create_user(
        username=username,
        password=password,
        email='carlos.moreno@example.com',
        first_name='Carlos',
        last_name='Moreno'
    )
    print(f"Usuario {username} creado exitosamente")

# Actualizar o crear perfil
profile, created = Profile.objects.get_or_create(
    user=user,
    defaults={
        'telefono': '3001234567',
        'documento': '12345678',
        'tipo_usuario': 'instructor',
        'tipo_naturaleza': 'natural',
        'biografia': 'Instructor con amplia experiencia en desarrollo frontend y backend. Especializado en React, Node.js y Python.',
        'linkedin': 'https://www.linkedin.com/in/carlos-moreno/',
        'twitter': 'https://twitter.com/carlosmoreno',
        'github': 'https://github.com/carlosmoreno',
        'sitio_web': 'https://carlosmoreno.dev',
        'esta_verificado': False
    }
)

if created:
    print("Perfil creado exitosamente")
else:
    # Actualizar perfil existente
    profile.telefono = '3001234567'
    profile.documento = '12345678'
    profile.tipo_usuario = 'instructor'
    profile.tipo_naturaleza = 'natural'
    profile.biografia = 'Instructor con amplia experiencia en desarrollo frontend y backend. Especializado en React, Node.js y Python.'
    profile.linkedin = 'https://www.linkedin.com/in/carlos-moreno/'
    profile.twitter = 'https://twitter.com/carlosmoreno'
    profile.github = 'https://github.com/carlosmoreno'
    profile.sitio_web = 'https://carlosmoreno.dev'
    profile.esta_verificado = False
    profile.save()
    print("Perfil actualizado exitosamente")

print("\n=== DATOS DE PRUEBA CREADOS ===")
print(f"Username: {username}")
print(f"Password: {password}")
print(f"Email: {user.email}")
print(f"Nombre: {user.first_name} {user.last_name}")
print("==================================")
print("\nPuedes usar estas credenciales en el frontend!")