from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Pokemon, Tipo, Favorito, Comentario, ImagenComunidad
from .forms import RegistroForm, LoginForm, ComentarioForm, ImagenForm
from django.contrib.auth.models import User




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
    ordenar    = request.GET.get('orden', '')

    if busqueda:
        pokemon = pokemon.filter(
            Q(nombre__icontains=busqueda) | Q(numero__icontains=busqueda)
        )
    if generacion:
        pokemon = pokemon.filter(generacion=generacion)
    if tipo_id:
        pokemon = pokemon.filter(Q(tipo1__id=tipo_id) | Q(tipo2__id=tipo_id))

    ORDEN_OPCIONES = {
        'numero':           'numero',
        'nombre':           'nombre',
        'hp':               '-hp',
        'ataque':           '-ataque',
        'ataque_especial':  '-ataque_especial',
        'defensa':          '-defensa',
        'defensa_especial': '-defensa_especial',
        'velocidad':        '-velocidad',
    }
    if ordenar in ORDEN_OPCIONES:
        pokemon = pokemon.order_by(ORDEN_OPCIONES[ordenar])

    return render(request, 'pokedex/lista.html', {
        'pokemon':      pokemon,
        'tipos':        tipos,
        'generaciones': Pokemon.GENERACIONES,
        'busqueda':     busqueda,
        'gen_activa':   generacion,
        'tipo_activo':  tipo_id,
        'orden_activo': ordenar,
        'total':        pokemon.count(),
    })


def detalle_pokemon(request, numero):
    pokemon     = get_object_or_404(Pokemon, numero=numero)
    comentarios = pokemon.comentarios.select_related('autor').all()
    imagenes = pokemon.imagenes.select_related('autor').filter(aprobada=True)

    es_favorito = False
    if request.user.is_authenticated:
        es_favorito = Favorito.objects.filter(
            entrenador=request.user, pokemon=pokemon
        ).exists()

    stats = [
        ('HP',               pokemon.hp,               round(pokemon.hp / 255 * 100)),
        ('Ataque',           pokemon.ataque,            round(pokemon.ataque / 255 * 100)),
        ('Ataque Especial',  pokemon.ataque_especial,   round(pokemon.ataque_especial / 255 * 100)),
        ('Defensa',          pokemon.defensa,           round(pokemon.defensa / 255 * 100)),
        ('Defensa Especial', pokemon.defensa_especial,  round(pokemon.defensa_especial / 255 * 100)),
        ('Velocidad',        pokemon.velocidad,         round(pokemon.velocidad / 255 * 100)),
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
    mis_imagenes = ImagenComunidad.objects.filter(
    autor=request.user
).select_related('pokemon')[:6]
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


@login_required
def mis_imagenes_estado(request):
    """El usuario ve si sus imágenes fueron aprobadas o están pendientes."""
    imagenes = ImagenComunidad.objects.filter(
        autor=request.user
    ).select_related('pokemon').order_by('-subida_en')
    return render(request, 'pokedex/mis_imagenes.html', {'imagenes': imagenes})

# ── Panel administrador propio ───────────────────────────────────

@staff_member_required(login_url='/login/')
def panel_admin(request):
    total_pokemon  = Pokemon.objects.count()
    total_usuarios = User.objects.count()
    imagenes_pend  = ImagenComunidad.objects.filter(aprobada=False).count()
    total_coment   = Comentario.objects.count()
    return render(request, 'pokedex/panel/index.html', {
        'total_pokemon':  total_pokemon,
        'total_usuarios': total_usuarios,
        'imagenes_pend':  imagenes_pend,
        'total_coment':   total_coment,
    })


@staff_member_required(login_url='/login/')
def panel_crear_pokemon(request):
    from .forms import PokemonForm
    if request.method == 'POST':
        form = PokemonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Pokémon creado correctamente.')
            return redirect('panel_admin')
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = PokemonForm()
    return render(request, 'pokedex/panel/pokemon_form.html', {
        'form':   form,
        'titulo': 'Crear Pokémon',
        'accion': 'Crear',
    })


@staff_member_required(login_url='/login/')
def panel_editar_pokemon(request, numero):
    from .forms import PokemonForm
    pokemon = get_object_or_404(Pokemon, numero=numero)
    if request.method == 'POST':
        form = PokemonForm(request.POST, instance=pokemon)
        if form.is_valid():
            form.save()
            messages.success(request, f'{pokemon.nombre} actualizado correctamente.')
            return redirect('panel_admin')
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = PokemonForm(instance=pokemon)
    return render(request, 'pokedex/panel/pokemon_form.html', {
        'form':    form,
        'titulo':  f'Editar — {pokemon.nombre}',
        'accion':  'Guardar cambios',
        'pokemon': pokemon,
    })


@staff_member_required(login_url='/login/')
def panel_eliminar_pokemon(request, numero):
    pokemon = get_object_or_404(Pokemon, numero=numero)
    if request.method == 'POST':
        nombre = pokemon.nombre
        pokemon.delete()
        messages.success(request, f'{nombre} eliminado correctamente.')
        return redirect('panel_admin')
    return render(request, 'pokedex/panel/pokemon_confirmar_eliminar.html', {
        'pokemon': pokemon,
    })


@staff_member_required(login_url='/login/')
def panel_lista_pokemon(request):
    busqueda = request.GET.get('q', '').strip()
    pokemon  = Pokemon.objects.select_related('tipo1', 'tipo2').all()
    if busqueda:
        pokemon = pokemon.filter(Q(nombre__icontains=busqueda) | Q(numero__icontains=busqueda))
    return render(request, 'pokedex/panel/pokemon_lista.html', {
        'pokemon':  pokemon,
        'busqueda': busqueda,
        'total':    pokemon.count(),
    })


@staff_member_required(login_url='/login/')
def panel_imagenes(request):
    pendientes = ImagenComunidad.objects.filter(aprobada=False).select_related('autor', 'pokemon')
    aprobadas  = ImagenComunidad.objects.filter(aprobada=True).select_related('autor', 'pokemon')
    return render(request, 'pokedex/panel/imagenes.html', {
        'pendientes': pendientes,
        'aprobadas':  aprobadas,
    })


@staff_member_required(login_url='/login/')
def panel_aprobar_imagen(request, pk):
    imagen = get_object_or_404(ImagenComunidad, pk=pk)
    imagen.aprobada = True
    imagen.save()
    messages.success(request, 'Imagen aprobada.')
    return redirect('panel_imagenes')


@staff_member_required(login_url='/login/')
def panel_rechazar_imagen(request, pk):
    imagen = get_object_or_404(ImagenComunidad, pk=pk)
    imagen.delete()
    messages.info(request, 'Imagen rechazada y eliminada.')
    return redirect('panel_imagenes')