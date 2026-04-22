from django import forms
from .models import Depoimento, Perfil

class DepoimentoForm(forms.ModelForm):
    class Meta:
        model = Depoimento
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Ex: Trabalhei com ele num projeto de C e ele causou um memory leak que travou o meu PC...'
            }),
        }
        labels = {
            'texto': 'Deixe um endosso de incompetência'
        }

class PerfilUpdateForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['titulo', 'localizacao']
        labels = {
            'titulo': 'Título Profissional',
            'localizacao': 'Localização'
        }