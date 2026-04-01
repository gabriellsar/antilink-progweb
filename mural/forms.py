from django import forms
from .models import Fracasso

class FracassoForm(forms.ModelForm):
    class Meta:
        model = Fracasso
        fields = ['titulo', 'descricao', 'nivel_vergonha', 'data_do_ocorrido', 'aprendizado']
        widgets = {
            'data_do_ocorrido': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }