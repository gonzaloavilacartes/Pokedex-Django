# Pokedex Django

Aplicación Django de catálogo y comunidad Pokémon con registro, búsqueda, filtros, favoritos, comentarios e imágenes de usuarios.

## Características

- Listado de Pokémon con búsqueda por nombre o número.
- Filtros por generación y tipo.
- Página de detalle con estadísticas, descripción y sprites oficiales.
- Registro e inicio de sesión de entrenadores.
- Funcionalidad de favoritos para cada usuario.
- Comentarios en cada ficha de Pokémon.
- Subida de imágenes comunitarias asociadas a cada Pokémon.
- Vista "Mi Pokedex" con favoritos, comentarios e imágenes del usuario.
- Comando custom `cargar_pokemon` para poblar la base de datos desde la PokeAPI.

## Requisitos

- Python 3.10+ (recomendado)
- Django 4.2
- Pillow
- requests

Instala las dependencias con:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

1. Ejecuta las migraciones:

```bash
python manage.py migrate
```

2. Crea un superusuario (opcional):

```bash
python manage.py createsuperuser
```

3. Carga Pokémon desde la PokeAPI:

```bash
python manage.py cargar_pokemon --limite 151
```

Puedes cambiar la cantidad con `--limite` y el punto de inicio con `--desde`.

## Uso

Inicia el servidor de desarrollo:

```bash
python manage.py runserver
```

Abre en tu navegador:

- `http://127.0.0.1:8000/` para la página principal
- `http://127.0.0.1:8000/pokemon/` para la lista completa
- `http://127.0.0.1:8000/registro/` para crear un usuario
- `http://127.0.0.1:8000/login/` para iniciar sesión

## Estructura del proyecto

- `pokedex/` - aplicación principal
  - `models.py` - definiciones de Pokémon, Tipo, Favorito, Comentario e ImagenComunidad
  - `views.py` - vistas públicas y privadas
  - `forms.py` - formularios de registro, login, comentario e imagen
  - `urls.py` - rutas de la aplicación
  - `management/commands/cargar_pokemon.py` - comando para poblar datos
- `pokedex_project/` - configuración global de Django
- `static/` - archivos estáticos
- `media/` - almacenamiento de imágenes subidas por usuarios

## Notas

- El proyecto usa SQLite (`db.sqlite3`) como base de datos por defecto.
- En producción debes configurar un `SECRET_KEY` seguro, `DEBUG = False`, y `ALLOWED_HOSTS` adecuados.
- Las imágenes de comunidad se guardan en `media/comunidad/`.
