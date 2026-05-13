import requests
from django.core.management.base import BaseCommand
from pokedex.models import Pokemon, Tipo

COLORES_TIPO = {
    'normal':   '#A8A878',
    'fire':     '#F08030',
    'water':    '#6890F0',
    'electric': '#F8D030',
    'grass':    '#78C850',
    'ice':      '#98D8D8',
    'fighting': '#C03028',
    'poison':   '#A040A0',
    'ground':   '#E0C068',
    'flying':   '#A890F0',
    'psychic':  '#F85888',
    'bug':      '#A8B820',
    'rock':     '#B8A038',
    'ghost':    '#705898',
    'dragon':   '#7038F8',
    'dark':     '#705848',
    'steel':    '#B8B8D0',
    'fairy':    '#EE99AC',
}

def get_generacion(numero):
    if numero <= 151:  return 1
    if numero <= 251:  return 2
    if numero <= 386:  return 3
    if numero <= 493:  return 4
    if numero <= 649:  return 5
    if numero <= 721:  return 6
    if numero <= 809:  return 7
    if numero <= 905:  return 8
    return 9

class Command(BaseCommand):
    help = 'Carga pokémon desde la PokeAPI a la base de datos SQLite'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limite',
            type=int,
            default=151,
            help='Cuántos pokémon cargar (default: 151)'
        )
        parser.add_argument(
            '--desde',
            type=int,
            default=1,
            help='Desde qué número empezar (default: 1)'
        )

    def handle(self, *args, **options):
        limite = options['limite']
        desde  = options['desde']
        hasta  = desde + limite - 1

        self.stdout.write(
            self.style.WARNING(f'\nCargando pokémon #{desde} al #{hasta}...\n')
        )

        cargados   = 0
        fallidos   = 0
        existentes = 0

        for numero in range(desde, hasta + 1):
            try:
                if Pokemon.objects.filter(numero=numero).exists():
                    self.stdout.write(f'  ⚠  #{numero} ya existe, saltando...')
                    existentes += 1
                    continue

                url      = f'https://pokeapi.co/api/v2/pokemon/{numero}'
                response = requests.get(url, timeout=10)

                if response.status_code != 200:
                    self.stdout.write(self.style.ERROR(f'  ✗  #{numero} no encontrado'))
                    fallidos += 1
                    continue

                data = response.json()

                descripcion = ''
                try:
                    sp_resp = requests.get(data['species']['url'], timeout=10)
                    sp_data = sp_resp.json()
                    for entry in sp_data.get('flavor_text_entries', []):
                        if entry['language']['name'] == 'es':
                            descripcion = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
                            break
                except Exception:
                    pass

                tipo1_obj = None
                tipo2_obj = None
                for t in data.get('types', []):
                    nombre_tipo = t['type']['name']
                    tipo_obj, _ = Tipo.objects.get_or_create(
                        nombre=nombre_tipo,
                        defaults={'color': COLORES_TIPO.get(nombre_tipo, '#888888')}
                    )
                    if t['slot'] == 1:
                        tipo1_obj = tipo_obj
                    elif t['slot'] == 2:
                        tipo2_obj = tipo_obj

                stats = {s['stat']['name']: s['base_stat'] for s in data.get('stats', [])}

                Pokemon.objects.create(
                    numero      = numero,
                    nombre      = data['name'].capitalize(),
                    descripcion = descripcion,
                    altura      = data.get('height', 0) / 10,
                    peso        = data.get('weight', 0) / 10,
                    hp          = stats.get('hp', 0),
                    ataque      = stats.get('attack', 0),
                    defensa     = stats.get('defense', 0),
                    velocidad   = stats.get('speed', 0),
                    generacion  = get_generacion(numero),
                    tipo1       = tipo1_obj,
                    tipo2       = tipo2_obj,
                )

                self.stdout.write(
                    self.style.SUCCESS(f'  ✓  #{numero} {data["name"].capitalize()} cargado')
                )
                cargados += 1

            except requests.exceptions.Timeout:
                self.stdout.write(self.style.ERROR(f'  ✗  #{numero} timeout, saltando...'))
                fallidos += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗  #{numero} error: {e}'))
                fallidos += 1

        self.stdout.write('\n' + '─' * 45)
        self.stdout.write(self.style.SUCCESS(f'  ✓  Cargados:    {cargados}'))
        if existentes:
            self.stdout.write(self.style.WARNING(f'  ⚠  Ya existían: {existentes}'))
        if fallidos:
            self.stdout.write(self.style.ERROR(f'  ✗  Fallidos:    {fallidos}'))
        self.stdout.write('─' * 45 + '\n')