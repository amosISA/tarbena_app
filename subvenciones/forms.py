# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.forms.models import inlineformset_factory

from .models import Subvencion, Estado, Area, Ente, Comment
from .sites import my_admin_site

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
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Overriding the default init method
        and setting the queryset of the area field
        to an empty list of choices
        """

        super().__init__(*args, **kwargs)
        self.fields['area'].queryset = Area.objects.none()

        if 'ente' in self.data:
            """ Create subvencion """
            try:
                ente_id = int(self.data.get('ente'))
                self.fields['area'].queryset = Area.objects.filter(ente_id=ente_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Area queryset
        elif self.instance.pk:
            """ Edit subvencion """
            self.fields['area'].queryset = self.instance.ente.area_set.order_by('nombre')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'contenido']

CommentFormSet = inlineformset_factory(Subvencion, Comment, form=CommentForm, extra=1, can_delete=False)