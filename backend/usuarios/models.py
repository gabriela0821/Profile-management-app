"""
Modelos para la gestión de usuarios y perfiles.
"""
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import URLValidator
import uuid
import os


def upload_profile_image(instance, filename):
    """Generar path para subida de imágenes de perfil"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex}.{ext}'
    return os.path.join('perfiles/', filename)


class Profile(models.Model):
    """
    Modelo extendido de perfil de usuario
    """
    TIPO_USUARIO_CHOICES = [
        ('instructor', 'Instructor'),
        ('estudiante', 'Estudiante'),
        ('admin', 'Administrador'),
    ]
    
    TIPO_NATURALEZA_CHOICES = [
        ('natural', 'Persona Natural'),
        ('juridica', 'Persona Jurídica'),
    ]
    
    # Relación con User
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    
    # Información personal
    telefono = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        help_text='Número de teléfono'
    )
    
    documento = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        help_text='Número de documento de identidad'
    )
    
    # Información profesional
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        default='instructor',
        help_text='Tipo de usuario en el sistema'
    )
    
    tipo_naturaleza = models.CharField(
        max_length=20,
        choices=TIPO_NATURALEZA_CHOICES,
        default='natural',
        help_text='Tipo de naturaleza jurídica'
    )
    
    biografia = models.TextField(
        blank=True, 
        null=True,
        max_length=500,
        help_text='Biografía del usuario'
    )
    
    # Imagen de perfil
    foto = models.ImageField(
        upload_to=upload_profile_image,
        blank=True,
        null=True,
        help_text='Foto de perfil del usuario'
    )
    
    # Enlaces sociales y web
    linkedin = models.URLField(
        blank=True, 
        null=True,
        help_text='Perfil de LinkedIn'
    )
    
    twitter = models.URLField(
        blank=True, 
        null=True,
        help_text='Perfil de Twitter'
    )
    
    github = models.URLField(
        blank=True, 
        null=True,
        help_text='Perfil de GitHub'
    )
    
    sitio_web = models.URLField(
        blank=True, 
        null=True,
        help_text='Sitio web personal'
    )
    
    # Estado del perfil
    esta_verificado = models.BooleanField(
        default=False,
        help_text='Indica si el perfil está verificado'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Perfil de {self.user.get_full_name() or self.user.username}'
    
    @property
    def full_name(self):
        """Retorna el nombre completo del usuario"""
        return f'{self.user.first_name} {self.user.last_name}'.strip()
    
    @property
    def foto_url(self):
        """Retorna la URL de la foto de perfil o None"""
        if self.foto:
            return self.foto.url
        return None
    
    def save(self, *args, **kwargs):
        """Override save para limpiar URLs vacías"""
        # Limpiar campos URL vacíos
        if self.linkedin == '':
            self.linkedin = None
        if self.twitter == '':
            self.twitter = None
        if self.github == '':
            self.github = None
        if self.sitio_web == '':
            self.sitio_web = None
            
        super().save(*args, **kwargs)


# Signal para crear perfil automáticamente
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crear perfil automáticamente cuando se crea un usuario"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Guardar perfil cuando se guarda el usuario"""
    if hasattr(instance, 'profile'):
        instance.profile.save()