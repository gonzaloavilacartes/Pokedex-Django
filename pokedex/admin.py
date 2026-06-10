from django.contrib import admin
from django.utils.html import format_html
from .models import Pokemon, Tipo, Favorito, Comentario, ImagenComunidad


@admin.register(Tipo)
class TipoAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'color', 'preview_color']
    search_fields = ['nombre']

    def preview_color(self, obj):
        return format_html(
            '<div style="width:30px;height:20px;background:{};border-radius:4px"></div>',
            obj.color
        )
    preview_color.short_description = 'Color'


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display   = ['numero', 'nombre', 'tipo1', 'tipo2', 'generacion',
                      'hp', 'ataque', 'ataque_especial',
                      'defensa', 'defensa_especial', 'velocidad']
    list_filter    = ['generacion', 'tipo1']
    search_fields  = ['nombre', 'numero']
    ordering       = ['numero']
    list_editable  = ['hp', 'ataque', 'ataque_especial',
                      'defensa', 'defensa_especial', 'velocidad']
    fieldsets = (
        ('Información básica', {
            'fields': ('numero', 'nombre', 'descripcion', 'generacion', 'tipo1', 'tipo2')
        }),
        ('Medidas', {
            'fields': ('altura', 'peso')
        }),
        ('Estadísticas base', {
            'fields': (
                ('hp',),
                ('ataque', 'ataque_especial'),
                ('defensa', 'defensa_especial'),
                ('velocidad',),
            )
        }),
    )


@admin.register(ImagenComunidad)
class ImagenComunidadAdmin(admin.ModelAdmin):
    list_display  = ['autor', 'pokemon', 'subida_en', 'aprobada', 'preview']
    list_filter   = ['aprobada']
    list_editable = ['aprobada']
    ordering      = ['aprobada', '-subida_en']
    actions       = ['aprobar_imagenes', 'rechazar_imagenes']

    def preview(self, obj):
        return format_html(
            '<img src="{}" style="height:50px;border-radius:6px"/>',
            obj.imagen.url
        )
    preview.short_description = 'Vista previa'

    def aprobar_imagenes(self, request, queryset):
        queryset.update(aprobada=True)
        self.message_user(request, f'{queryset.count()} imagen(es) aprobada(s).')
    aprobar_imagenes.short_description = '✓ Aprobar imágenes seleccionadas'

    def rechazar_imagenes(self, request, queryset):
        queryset.update(aprobada=False)
        self.message_user(request, f'{queryset.count()} imagen(es) rechazada(s).')
    rechazar_imagenes.short_description = '✗ Rechazar imágenes seleccionadas'


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display  = ['autor', 'pokemon', 'texto', 'creado_en']
    list_filter   = ['pokemon']
    search_fields = ['autor__username', 'texto']


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ['entrenador', 'pokemon', 'fecha']