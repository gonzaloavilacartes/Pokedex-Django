from django.db import models
from django.contrib.auth.models import User


class Tipo(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    color  = models.CharField(max_length=7, default='#888888')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'
        ordering = ['nombre']


class Pokemon(models.Model):
    GENERACIONES = [
        (1, 'Gen I — 1996'),
        (2, 'Gen II — 1999'),
        (3, 'Gen III — 2002'),
        (4, 'Gen IV — 2006'),
        (5, 'Gen V — 2010'),
        (6, 'Gen VI — 2013'),
        (7, 'Gen VII — 2016'),
        (8, 'Gen VIII — 2019'),
        (9, 'Gen IX — 2022'),
    ]

    numero      = models.IntegerField(unique=True)
    nombre      = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    altura      = models.FloatField(default=0)
    peso        = models.FloatField(default=0)
    hp          = models.IntegerField(default=0)
    ataque      = models.IntegerField(default=0)
    defensa     = models.IntegerField(default=0)
    velocidad   = models.IntegerField(default=0)
    generacion  = models.IntegerField(choices=GENERACIONES, default=1)
    tipo1       = models.ForeignKey(
        Tipo, on_delete=models.SET_NULL, null=True,
        related_name='pokemon_tipo1'
    )
    tipo2       = models.ForeignKey(
        Tipo, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='pokemon_tipo2'
    )

    def __str__(self):
        return f'#{self.numero} {self.nombre}'

    def get_imagen(self):
        return f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{self.numero}.png'

    def get_sprite(self):
        return f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{self.numero}.png'

    def get_anio(self):
        anios = {1:1996,2:1999,3:2002,4:2006,5:2010,6:2013,7:2016,8:2019,9:2022}
        return anios.get(self.generacion, '')

    class Meta:
        verbose_name = 'Pokémon'
        verbose_name_plural = 'Pokémon'
        ordering = ['numero']


class Favorito(models.Model):
    entrenador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoritos')
    pokemon    = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='favoritos')
    fecha      = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('entrenador', 'pokemon')
        verbose_name = 'Favorito'

    def __str__(self):
        return f'{self.entrenador.username} → {self.pokemon.nombre}'


class Comentario(models.Model):
    autor     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios')
    pokemon   = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='comentarios')
    texto     = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['-creado_en']

    def __str__(self):
        return f'{self.autor.username} sobre {self.pokemon.nombre}'


class ImagenComunidad(models.Model):
    autor       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='imagenes')
    pokemon     = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='imagenes')
    imagen      = models.ImageField(upload_to='comunidad/')
    descripcion = models.CharField(max_length=200, blank=True)
    subida_en   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Imagen comunidad'
        verbose_name_plural = 'Imágenes comunidad'
        ordering = ['-subida_en']

    def __str__(self):
        return f'{self.autor.username} → {self.pokemon.nombre}'