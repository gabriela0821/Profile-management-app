"""
Configuración del panel de administración
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    """Inline para mostrar perfil en usuario"""
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil'
    extra = 0
    fieldsets = (
        ('Información Personal', {
            'fields': ('telefono', 'documento', 'biografia')
        }),
        ('Información Profesional', {
            'fields': ('tipo_usuario', 'tipo_naturaleza', 'esta_verificado')
        }),
        ('Enlaces Sociales', {
            'fields': ('linkedin', 'twitter', 'github', 'sitio_web'),
            'classes': ('collapse',)
        }),
        ('Imagen', {
            'fields': ('foto',)
        }),
    )


class CustomUserAdmin(UserAdmin):
    """Administrador personalizado de usuarios"""
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_tipo_usuario')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__tipo_usuario')
    
    def get_tipo_usuario(self, obj):
        """Obtener tipo de usuario del perfil"""
        if hasattr(obj, 'profile'):
            return obj.profile.get_tipo_usuario_display()
        return 'Sin perfil'
    get_tipo_usuario.short_description = 'Tipo Usuario'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Administrador de perfiles"""
    list_display = (
        'user', 'get_full_name', 'tipo_usuario', 'tipo_naturaleza', 
        'telefono', 'esta_verificado', 'created_at'
    )
    list_filter = ('tipo_usuario', 'tipo_naturaleza', 'esta_verificado', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'telefono')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Información Personal', {
            'fields': ('telefono', 'documento', 'biografia')
        }),
        ('Información Profesional', {
            'fields': ('tipo_usuario', 'tipo_naturaleza', 'esta_verificado')
        }),
        ('Enlaces Sociales', {
            'fields': ('linkedin', 'twitter', 'github', 'sitio_web'),
            'classes': ('collapse',)
        }),
        ('Imagen', {
            'fields': ('foto',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        """Obtener nombre completo"""
        return obj.full_name or 'Sin nombre'
    get_full_name.short_description = 'Nombre Completo'


# Re-registrar UserAdmin con la configuración personalizada
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Personalizar títulos del admin
admin.site.site_header = 'Administración - Prueba Técnica'
admin.site.site_title = 'Admin Prueba Técnica'
admin.site.index_title = 'Panel de Administración'