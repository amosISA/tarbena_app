# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper

from .models import Parcela
from .sites import my_admin_site

class ParcelaForm(forms.ModelForm):
    class Meta:
        model = Parcela
        fields = '__all__'