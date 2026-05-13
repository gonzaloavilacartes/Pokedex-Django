from django.urls import path
from . import views

urlpatterns = [
    # Publicas
    path('',                          views.index,            name='index'),
    path('pokemon/',                  views.lista_pokemon,    name='lista_pokemon'),
    path('pokemon/<int:numero>/',     views.detalle_pokemon,  name='detalle_pokemon'),

    # Autenticación
    path('registro/',                 views.registro,         name='registro'),
    path('login/',                    views.login_view,       name='login'),
    path('logout/',                   views.logout_view,      name='logout'),

    # Privadas
    path('mi-pokedex/',               views.mi_pokedex,       name='mi_pokedex'),
    path('pokemon/<int:numero>/favorito/',      views.toggle_favorito,     name='toggle_favorito'),
    path('pokemon/<int:numero>/comentar/',      views.comentar,            name='comentar'),
    path('pokemon/<int:numero>/subir-imagen/',  views.subir_imagen,        name='subir_imagen'),
    path('comentario/<int:pk>/eliminar/',       views.eliminar_comentario, name='eliminar_comentario'),
]