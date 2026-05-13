# Pokedex Django

Aplicación web Django para gestionar una Pokédex local con búsqueda, filtros, favoritos, comentarios y subida de imágenes de la comunidad.

## Características

- Lista de Pokémon con filtros por nombre, número, generación y tipo.
- Página de detalle de cada Pokémon con estadísticas, comentarios e imágenes de comunidad.
- Registro, inicio de sesión y control de sesiones.
- Perfil `Mi Pokedex` con favoritos, comentarios propios e imágenes subidas.
- Importación de Pokémon desde la PokeAPI mediante comando personalizado.
- Uso de SQLite como base de datos local.

## Requisitos

- Python 3.11+ (compatible con Django 4.2+)
- Dependencias en `requirements.txt`

## Instalación

1. Crear un entorno virtual:
   ```bash
   python -m venv venv
   ```

2. Activar el entorno virtual:
   - Windows PowerShell:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Windows CMD:
     ```cmd
     .\venv\Scripts\activate
     ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Crear migraciones y aplicar la base de datos:
   ```bash
   python manage.py migrate
   ```

5. (Opcional) Crear un superusuario para acceder al admin de Django:
   ```bash
   python manage.py createsuperuser
   ```

## Cargar datos de Pokémon

La aplicación incluye un comando personalizado para descargar datos desde PokeAPI.

Ejemplo:
```bash
python manage.py cargar_pokemon --desde 1 --limite 151
```

Esto genera los Pokémon en la base de datos y crea los tipos asociados.

## Ejecutar el servidor

```bash
python manage.py runserver
```

Luego abrir en el navegador:

- `http://127.0.0.1:8000/` — Página principal
- `http://127.0.0.1:8000/pokemon/` — Lista de Pokémon
- `http://127.0.0.1:8000/login/` — Inicio de sesión
- `http://127.0.0.1:8000/registro/` — Registro de usuario
- `http://127.0.0.1:8000/mi-pokedex/` — Perfil de usuario

## Estructura del proyecto

- `pokedex/` — App principal con modelos, vistas, formularios y plantillas.
- `pokedex_project/` — Configuración global de Django.
- `static/` — Archivos estáticos (CSS, imágenes, etc.).
- `media/` — Archivos cargados por usuarios.
- `db.sqlite3` — Base de datos local SQLite.

## Configuración adicional

- `MEDIA_URL` y `MEDIA_ROOT` ya están configurados para servir archivos subidos durante el desarrollo.
- `STATICFILES_DIRS` apunta a `static/`.
- La app usa `LOGIN_URL`, `LOGIN_REDIRECT_URL` y `LOGOUT_REDIRECT_URL` para manejar la autenticación.

## Notas

- El proyecto está configurado en modo `DEBUG = True` y `ALLOWED_HOSTS = ['*']`, adecuado para desarrollo pero no para producción.
- Si se desea usar el admin de Django, cargar al menos un usuario con `createsuperuser`.
- Para subir imágenes de comunidad se requiere autenticación de usuario.
