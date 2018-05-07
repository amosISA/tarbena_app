# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from .models import Subvencion

@login_required()
def index_subvenciones(request):
    return render(request,
                  'subvenciones/index.html',
                  {})
