# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.forms.models import inlineformset_factory

from .models import Subvencion, Estado, Area, Ente, Comment
from .sites import my_admin_site

import django_filters

class EstadoForm(forms.ModelForm):
    class Meta:
        model = Estado
        fields = ["nombre"]

class EnteForm(forms.ModelForm):
    class Meta:
        model = Ente
        fields = ["nombre"]

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ["nombre", "ente"]

class SubvencionFilter(django_filters.FilterSet):
    estado = django_filters.filters.ModelMultipleChoiceFilter(
        field_name='estado__nombre',
        to_field_name='nombre',
        queryset=Estado.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Subvencion
        fields = ['ente', 'area', 'responsable']

class SubvencionForm(forms.ModelForm):
    class Meta:
        model = Subvencion
        fields = '__all__'
        widgets = {
            'fecha_publicacion': forms.DateInput(format='%Y-%m-%d', attrs={'type':'date'}),
            'fin': forms.DateInput(format='%Y-%m-%d', attrs={'type':'date'}),
            'fecha_resolucion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'estado': RelatedFieldWidgetWrapper(
                Subvencion._meta.get_field('estado').formfield().widget,
                Subvencion._meta.get_field('estado').rel,
                my_admin_site,
                can_add_related=True
            ),
            'ente': RelatedFieldWidgetWrapper(
                Subvencion._meta.get_field('ente').formfield().widget,
                Subvencion._meta.get_field('ente').rel,
                my_admin_site,
                can_add_related=True
            ),
            'area': RelatedFieldWidgetWrapper(
                Subvencion._meta.get_field('area').formfield().widget,
                Subvencion._meta.get_field('area').rel,
                my_admin_site,
                can_add_related=True
            ),
            'se_relaciona_con': forms.CheckboxSelectMultiple(),
            'responsable': forms.CheckboxSelectMultiple(),
            'colectivo': forms.CheckboxSelectMultiple(),
        }
        exclude = ('user', 'likes',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'contenido']

CommentFormSet = inlineformset_factory(Subvencion, Comment, form=CommentForm, extra=1, can_delete=False)