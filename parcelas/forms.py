# -*- coding: utf-8 -*-
from dal import autocomplete
from django import forms
from django.contrib.auth.models import User

from .models import Parcela, Propietario

class ParcelaForm(forms.ModelForm):
    propietario = forms.ModelChoiceField(
        queryset=Propietario.objects.all(),
        widget=autocomplete.ModelSelect2(url='parcelas:propietario-autocomplete')
    )

    class Meta:
        model = Parcela
        fields = '__all__'