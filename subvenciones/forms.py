# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
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
    fecha_publicacion = django_filters.CharFilter(
        label='Año inicio',
        lookup_expr='icontains',
    )
    fin = django_filters.CharFilter(
        label='Año fin',
        lookup_expr='icontains',
    )
    estado = django_filters.filters.ModelMultipleChoiceFilter(
        label='Estado',
        field_name='estado__nombre',
        to_field_name='nombre',
        queryset=Estado.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    responsable = django_filters.filters.ModelMultipleChoiceFilter(
        label='Responsable',
        field_name='responsable__first_name',
        to_field_name='first_name',
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Subvencion
        fields = ['ente', 'area']

class SubvencionForm(forms.ModelForm):
    # In reponsable field get user by first_name
    def __init__(self, *args, **kwargs):
        super(SubvencionForm, self).__init__(*args, **kwargs)
        users = User.objects.all()
        self.fields['responsable'].choices = [(user.pk, user.first_name) for user in users]

    class Meta:
        model = Subvencion
        fields = '__all__'
        widgets = {
            'fecha_publicacion': forms.DateInput(format='%Y-%m-%d', attrs={'type':'date'}),
            'fin': forms.DateInput(format='%Y-%m-%d', attrs={'type':'date'}),
            'fecha_resolucion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'incio_ejecucion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fin_ejecucion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fin_justificacion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fecha_envio': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            # 'estado': RelatedFieldWidgetWrapper(
            #     Subvencion._meta.get_field('estado').formfield().widget,
            #     Subvencion._meta.get_field('estado').rel,
            #     my_admin_site,
            #     can_add_related=True
            # ),
            # 'ente': RelatedFieldWidgetWrapper(
            #     Subvencion._meta.get_field('ente').formfield().widget,
            #     Subvencion._meta.get_field('ente').rel,
            #     my_admin_site,
            #     can_add_related=True
            # ),
            # 'area': RelatedFieldWidgetWrapper(
            #     Subvencion._meta.get_field('area').formfield().widget,
            #     Subvencion._meta.get_field('area').rel,
            #     my_admin_site,
            #     can_add_related=True
            # ),
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