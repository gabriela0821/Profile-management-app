# 🧪 Aplicación de Gestión de Perfil - Prueba Técnica Frontend

Una aplicación moderna de gestión de perfiles desarrollada con **React**, **Next.js** y **TypeScript**, que implementa autenticación JWT y todas las funcionalidades solicitadas en la prueba técnica.

![Demo](https://img.shields.io/badge/Demo-Live-green)
![React](https://img.shields.io/badge/React-18-blue)
![Next.js](https://img.shields.io/badge/Next.js-15-black)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)

## 🎯 Descripción

Esta aplicación permite a los usuarios:
- ✅ **Autenticarse** con JWT (access y refresh tokens)
- ✅ **Visualizar** su perfil completo con toda la información
- ✅ **Editar** todos los campos del perfil de manera intuitiva
- ✅ **Subir y actualizar** su foto de perfil con vista previa
- ✅ **Navegación fluida** con diseño responsive y moderno

## 🚀 Instalación y Configuración

### Prerrequisitos
- **Node.js** 18.0 o superior
- **Python** 3.8+ (para el backend)
- **npm** o **yarn**

### Instalación del Frontend

```bash
# Clonar el repositorio
git clone [URL-del-repositorio]
cd profile-management-app

# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev

```
### Instalación del Backend

```bash

# Navegar a la carpeta backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Crear usuario de prueba
python manage.py shell
# Dentro del shell:
from django.contrib.auth.models import User
User.objects.create_user(username='carlosandresmoreno', password='90122856_Hanz', first_name='Carlos', last_name='Moreno', email='carlos@example.com')
exit()

# Ejecutar servidor backend
python manage.py runserver 8010
