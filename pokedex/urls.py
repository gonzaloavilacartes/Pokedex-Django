from django.urls import path
from . import views

urlpatterns = [
    # publi
    path('',                          views.index,            name='index'),
    path('pokemon/',                  views.lista_pokemon,    name='lista_pokemon'),
    path('pokemon/<int:numero>/',     views.detalle_pokemon,  name='detalle_pokemon'),

    # inicio
    path('registro/',                 views.registro,         name='registro'),
    path('login/',                    views.login_view,       name='login'),
    path('logout/',                   views.logout_view,      name='logout'),

    # priv 
    path('mi-pokedex/',               views.mi_pokedex,           name='mi_pokedex'),
    path('mis-imagenes/',             views.mis_imagenes_estado,  name='mis_imagenes'),
    path('pokemon/<int:numero>/favorito/',     views.toggle_favorito,     name='toggle_favorito'),
    path('pokemon/<int:numero>/comentar/',     views.comentar,            name='comentar'),
    path('pokemon/<int:numero>/subir-imagen/', views.subir_imagen,        name='subir_imagen'),
    path('comentario/<int:pk>/eliminar/',      views.eliminar_comentario, name='eliminar_comentario'),

    # paneles admin
    path('admin-panel/',                              views.panel_admin,              name='panel_admin'),
    path('admin-panel/pokemon/',                      views.panel_lista_pokemon,      name='panel_lista_pokemon'),
    path('admin-panel/pokemon/crear/',                views.panel_crear_pokemon,      name='panel_crear_pokemon'),
    path('admin-panel/pokemon/<int:numero>/editar/',  views.panel_editar_pokemon,     name='panel_editar_pokemon'),
    path('admin-panel/pokemon/<int:numero>/eliminar/',views.panel_eliminar_pokemon,   name='panel_eliminar_pokemon'),
    path('admin-panel/imagenes/',                     views.panel_imagenes,           name='panel_imagenes'),
    path('admin-panel/imagenes/<int:pk>/aprobar/',    views.panel_aprobar_imagen,     name='panel_aprobar_imagen'),
    path('admin-panel/imagenes/<int:pk>/rechazar/',   views.panel_rechazar_imagen,    name='panel_rechazar_imagen'),
]