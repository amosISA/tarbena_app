import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import GrupoComponentes, Componentes, Incidencias

class MaquinaIncidenciasForm(forms.ModelForm):
    class Meta:
        model = Incidencias
        fields = ["tipo_incidencias", "fecha", "cerrado", "comentario", "mantenimientos",]
        widgets = {
            'tipo_incidencias': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.TextInput(attrs={'class': 'form-control .fecha', 'autocomplete': 'off'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control .comentario'}),
            'mantenimientos': forms.Select(attrs={'class': 'form-control'}),
        }

class GrupoComponentesForm(forms.ModelForm):
    class Meta:
        model = GrupoComponentes
        fields = ["tipo_grupo_componentes"]

class ComponentesForm(forms.ModelForm):
    class Meta:
        model = Componentes
        fields = ["tipo_componentes"]

