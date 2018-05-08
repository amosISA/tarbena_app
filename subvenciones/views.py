# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import SubvencionForm
from .models import Subvencion, Estado, Colectivo, Area

@login_required()
def index_subvenciones(request, estado_slug=None):
    """ List subvenciones """

    estado, area, user = None, None, None
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
        elif Area.objects.filter(slug=estado_slug).exists():
            area = get_object_or_404(Area, slug=estado_slug)
            subvenciones = subvenciones.filter(ente__area=area)
        elif User.objects.filter(username=estado_slug).exists():
            user = get_object_or_404(User, username=estado_slug)
            subvenciones = subvenciones.filter(responsable__username=user)
        else:
            subvenciones = Subvencion.objects.all()

    days_until_estado = ['7d', '6d', '5d', '4d', '3d', '2d', '1d', 'expires today', 'expired']

    return render(request,
                  'subvenciones/index.html',
                  {'estado': estado,
                   'area': area,
                   'user': user,
                   'estados': estados,
                   'subvenciones': subvenciones,
                   'days_until_estado': days_until_estado,
                   'total_subvenciones': total_subvenciones,
                   'colectivos': colectivos})

# Load a list of areas for a given Ente
def load_areas(request):
    ente_id = request.GET.get('ente')
    areas = Area.objects.filter(ente_id=ente_id).order_by('nombre')
    return render(request, 'subvenciones/areas_dropdown_list_options.html', {'areas': areas})

# --------------- Create New Subsidie --------------- #
class SubvencionCreateView(LoginRequiredMixin, CreateView):
    form_class = SubvencionForm
    template_name = 'subvenciones/create.html'
    success_url = reverse_lazy('subvenciones:index')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        messages.success(self.request, 'Subvención añadida correctamente')
        return super(SubvencionCreateView, self).form_valid(form)