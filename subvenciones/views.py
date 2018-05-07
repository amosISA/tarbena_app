# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from .models import Subvencion, Estado, Colectivo

@login_required()
def index_subvenciones(request, estado_slug=None):
    """ List subvenciones """

    estado = None
    estados = Estado.objects.all().annotate(number_stats=Count('subvencion'))

    # If is superuser: list all subsidies, if not, only the related to the respective user
    if request.user.is_superuser:
        subvenciones = Subvencion.objects.extra(select={"day_mod": "date(fin)"}).order_by('day_mod')
    else:
        subvenciones = Subvencion.objects.all().filter(user=request.user)

    total_subvenciones = Subvencion.objects.count()
    colectivos = Colectivo.objects.all()

    if estado_slug:
        if Estado.objects.filter(slug=estado_slug).exists():
            estado = get_object_or_404(Estado, slug=estado_slug)
            subvenciones = subvenciones.filter(estado=estado)
        else:
            subvenciones = Subvencion.objects.all()

    days_until_estado = ['7d', '6d', '5d', '4d', '3d', '2d', '1d', 'expires today', 'expired']

    return render(request,
                  'subvenciones/index.html',
                  {'estado': estado,
                   'estados': estados,
                   'subvenciones': subvenciones,
                   'days_until_estado': days_until_estado,
                   'total_subvenciones': total_subvenciones,
                   'colectivos': colectivos})
