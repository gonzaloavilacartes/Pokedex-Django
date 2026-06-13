from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Comentario, ImagenComunidad, Pokemon


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo electrónico')

    class Meta:
        model  = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username':  'Nombre de entrenador',
            'email':     'correo@ejemplo.com',
            'password1': 'Contraseña',
            'password2': 'Repite la contraseña',
        }
        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholders.get(name, ''),
            })
            field.help_text = ''


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nombre de usuario',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña',
        })


class ComentarioForm(forms.ModelForm):
    class Meta:
        model  = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escribe tu comentario sobre este Pokémon...',
            })
        }
        labels = {'texto': ''}


class ImagenForm(forms.ModelForm):
    class Meta:
        model  = ImagenComunidad
        fields = ['imagen', 'descripcion']
        widgets = {
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción opcional...',
            }),
        }
        labels = {
            'imagen':      'Selecciona una imagen',
            'descripcion': 'Descripción',
        }
     
        
class PokemonForm(forms.ModelForm):
    class Meta:
        model  = Pokemon
        fields = [
            'numero', 'nombre', 'descripcion', 'generacion',
            'tipo1', 'tipo2', 'altura', 'peso',
            'hp', 'ataque', 'ataque_especial',
            'defensa', 'defensa_especial', 'velocidad'
        ]
        widgets = {
            'numero':      forms.NumberInput(attrs={'class': 'form-control'}),
            'nombre':      forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'generacion':  forms.Select(attrs={'class': 'form-select'}),
            'tipo1':       forms.Select(attrs={'class': 'form-select'}),
            'tipo2':       forms.Select(attrs={'class': 'form-select'}),
            'altura':      forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'peso':        forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'hp':               forms.NumberInput(attrs={'class': 'form-control'}),
            'ataque':           forms.NumberInput(attrs={'class': 'form-control'}),
            'ataque_especial':  forms.NumberInput(attrs={'class': 'form-control'}),
            'defensa':          forms.NumberInput(attrs={'class': 'form-control'}),
            'defensa_especial': forms.NumberInput(attrs={'class': 'form-control'}),
            'velocidad':        forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'numero':           'Número',
            'nombre':           'Nombre',
            'descripcion':      'Descripción',
            'generacion':       'Generación',
            'tipo1':            'Tipo primario',
            'tipo2':            'Tipo secundario',
            'altura':           'Altura (m)',
            'peso':             'Peso (kg)',
            'hp':               'HP',
            'ataque':           'Ataque',
            'ataque_especial':  'Ataque Especial',
            'defensa':          'Defensa',
            'defensa_especial': 'Defensa Especial',
            'velocidad':        'Velocidad',
        }