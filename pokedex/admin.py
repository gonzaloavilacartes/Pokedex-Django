from django.contrib import admin
from .models import Pokemon, Tipo, Favorito, Comentario, ImagenComunidad


@admin.register(Tipo)
class TipoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'color']


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display  = ['numero', 'nombre', 'tipo1', 'tipo2', 'generacion']
    list_filter   = ['generacion', 'tipo1']
    search_fields = ['nombre', 'numero']
    ordering      = ['numero']


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['autor', 'pokemon', 'creado_en']
    list_filter  = ['pokemon']


@admin.register(ImagenComunidad)
class ImagenAdmin(admin.ModelAdmin):
    list_display = ['autor', 'pokemon', 'subida_en']


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ['entrenador', 'pokemon', 'fecha']