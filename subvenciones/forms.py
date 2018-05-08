# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper

from .models import Subvencion, Estado, Area, Ente
from .sites import my_admin_site

class EstadoForm(forms.ModelForm):
    class Meta:
        model = Estado
        fields = ["nombre"]

class EnteForm(forms.ModelForm):
    class Meta:
        model = Ente
        fields = ["nombre", "area"]

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ["nombre"]

class SubvencionForm(forms.ModelForm):
    class Meta:
        model = Subvencion
        fields = '__all__'
        widgets = {
            'inicio': forms.DateInput(format='%Y-%m-%d', attrs={'type':'date'}),
            'fin': forms.DateInput(format='%Y-%m-%d', attrs={'type':'date'}),
            'estado': RelatedFieldWidgetWrapper(
                Subvencion._meta.get_field('estado').formfield().widget,
                Subvencion._meta.get_field('estado').rel,
                my_admin_site,
                can_add_related=True
            ),
            'responsable': RelatedFieldWidgetWrapper(
                Subvencion._meta.get_field('responsable').formfield().widget,
                Subvencion._meta.get_field('responsable').rel,
                my_admin_site,
                can_add_related=True
            ),
            'se_relaciona_con': forms.CheckboxSelectMultiple(),
            'responsable': forms.CheckboxSelectMultiple(),
            'colectivo': forms.CheckboxSelectMultiple(),
        }
        exclude = ('user',)