from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Pokemon, Tipo, Favorito, Comentario, ImagenComunidad
from .forms import RegistroForm, LoginForm, ComentarioForm, ImagenForm



def index(request):
    pokemon_destacados = Pokemon.objects.all()[:12]
    generaciones = Pokemon.GENERACIONES
    return render(request, 'pokedex/index.html', {
        'pokemon_destacados': pokemon_destacados,
        'generaciones': generaciones,
    })


def lista_pokemon(request):
    pokemon = Pokemon.objects.select_related('tipo1', 'tipo2').all()
    tipos   = Tipo.objects.all()

    busqueda   = request.GET.get('q', '').strip()
    generacion = request.GET.get('gen', '')
    tipo_id    = request.GET.get('tipo', '')

    if busqueda:
        pokemon = pokemon.filter(
            Q(nombre__icontains=busqueda) | Q(numero__icontains=busqueda)
        )
    if generacion:
        pokemon = pokemon.filter(generacion=generacion)
    if tipo_id:
        pokemon = pokemon.filter(Q(tipo1__id=tipo_id) | Q(tipo2__id=tipo_id))

    return render(request, 'pokedex/lista.html', {
        'pokemon':     pokemon,
        'tipos':       tipos,
        'generaciones': Pokemon.GENERACIONES,
        'busqueda':    busqueda,
        'gen_activa':  generacion,
        'tipo_activo': tipo_id,
        'total':       pokemon.count(),
    })


def detalle_pokemon(request, numero):
    pokemon     = get_object_or_404(Pokemon, numero=numero)
    comentarios = pokemon.comentarios.select_related('autor').all()
    imagenes    = pokemon.imagenes.select_related('autor').all()

    es_favorito = False
    if request.user.is_authenticated:
        es_favorito = Favorito.objects.filter(
            entrenador=request.user, pokemon=pokemon
        ).exists()

    stats = [
        ('HP',        pokemon.hp,        round(pokemon.hp / 255 * 100)),
        ('Ataque',    pokemon.ataque,     round(pokemon.ataque / 255 * 100)),
        ('Defensa',   pokemon.defensa,    round(pokemon.defensa / 255 * 100)),
        ('Velocidad', pokemon.velocidad,  round(pokemon.velocidad / 255 * 100)),
    ]

    return render(request, 'pokedex/detalle.html', {
        'pokemon':         pokemon,
        'comentarios':     comentarios,
        'imagenes':        imagenes,
        'es_favorito':     es_favorito,
        'comentario_form': ComentarioForm(),
        'imagen_form':     ImagenForm(),
        'stats':           stats,
    })



def registro(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido, entrenador {user.username}!')
            return redirect('index')
    else:
        form = RegistroForm()
    return render(request, 'pokedex/registro.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, f'¡Bienvenido de vuelta, {form.get_user().username}!')
            return redirect(request.GET.get('next', 'index'))
        messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'pokedex/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada.')
    return redirect('index')



@login_required
def mi_pokedex(request):
    favoritos = Favorito.objects.filter(
        entrenador=request.user
    ).select_related('pokemon', 'pokemon__tipo1', 'pokemon__tipo2')
    mis_comentarios = Comentario.objects.filter(autor=request.user).select_related('pokemon')[:5]
    mis_imagenes    = ImagenComunidad.objects.filter(autor=request.user).select_related('pokemon')[:6]
    return render(request, 'pokedex/mi_pokedex.html', {
        'favoritos':       favoritos,
        'mis_comentarios': mis_comentarios,
        'mis_imagenes':    mis_imagenes,
    })


@login_required
def toggle_favorito(request, numero):
    pokemon  = get_object_or_404(Pokemon, numero=numero)
    fav = Favorito.objects.filter(entrenador=request.user, pokemon=pokemon)
    if fav.exists():
        fav.delete()
        messages.info(request, f'{pokemon.nombre} eliminado de favoritos.')
    else:
        Favorito.objects.create(entrenador=request.user, pokemon=pokemon)
        messages.success(request, f'{pokemon.nombre} añadido a favoritos.')
    return redirect('detalle_pokemon', numero=numero)


@login_required
def comentar(request, numero):
    pokemon = get_object_or_404(Pokemon, numero=numero)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.autor = request.user
            c.pokemon = pokemon
            c.save()
            messages.success(request, 'Comentario publicado.')
    return redirect('detalle_pokemon', numero=numero)


@login_required
def eliminar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk, autor=request.user)
    numero = comentario.pokemon.numero
    comentario.delete()
    messages.info(request, 'Comentario eliminado.')
    return redirect('detalle_pokemon', numero=numero)


@login_required
def subir_imagen(request, numero):
    pokemon = get_object_or_404(Pokemon, numero=numero)
    if request.method == 'POST':
        form = ImagenForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.autor   = request.user
            img.pokemon = pokemon
            img.save()
            messages.success(request, 'Imagen subida.')
    return redirect('detalle_pokemon', numero=numero)