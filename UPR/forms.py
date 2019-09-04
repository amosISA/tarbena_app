import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import GrupoComponentes, Componentes, Incidencias, MovimientoMaquinaria, MovimientoObra


# formularios para incidencias.html | MaquinaIncidenciasForm, GrupoComponentesForm, ComponentesForm
class MaquinaIncidenciasForm(forms.ModelForm):
    class Meta:
        model = Incidencias
        fields = ["tipo_incidencias", "fecha", "cerrado", "taller", "comentario", "mantenimientos", "n_inventario", "campo_componente"]
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
     #   widgets = {
     #       'tipo_comentario': forms.Textarea(attrs={'class': 'form-control', 'disable': 'disabled'}),
     #   }

# formluarios para Ubicacion | MovimientoMaquinaria

class MovimientoMaquinariaForm(forms.ModelForm):
    class Meta:
        model = MovimientoMaquinaria
        fields = ["fecha_movimiento", "comentario", "poblacion_mm"]
        widgets = {
            'fecha_movimiento': forms.TextInput(attrs={'class': 'form-control .fecha', 'autocomplete': 'off'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control .comentario'}),
            'poblacion': forms.Select(attrs={'class': 'form-control'}),
        }
class MovimientoObraForm(forms.ModelForm):
    class Meta:
        model = MovimientoObra
        fields = ["fecha_movimiento", "comentario", "nombre_obra"]
        widgets = {
            'fecha_movimiento': forms.TextInput(attrs={'class': 'form-control .fecha', 'autocomplete': 'off'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control .comentario'}),
            'nombre_obra': forms.Select(attrs={'class': 'form-control'}),
        }
