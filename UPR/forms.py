import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import GrupoComponentes, Componentes, Incidencias

class MaquinaIncidenciasForm(forms.ModelForm):
    class Meta:
        model = Incidencias
        fields = ["tipo_incidencias", "fecha", "cerrado", "comentario", "mantenimientos",]

class GrupoComponentesForm(forms.ModelForm):
    class Meta:
        model = GrupoComponentes
        fields = ["tipo_grupo_componentes"]

class ComponentesForm(forms.ModelForm):
    class Meta:
        model = Componentes
        fields = ["tipo_componentes"]

