# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView

from .forms import RegisterForm

import sys
sys.path.append("..")
from subvenciones.models import Subvencion
from favourites.models import Favourite

# --------------- Index --------------- #
def index(request):
    if request.user.is_authenticated():
        favourites = Favourite.objects.all().prefetch_related('user').select_related('type')
        return render(request, 'home/index.html', {'favourites': favourites})
    else:
        return HttpResponseRedirect(reverse('login'))

# --------------- Subvenciones Transparencia --------------- #
def index_subvenciones_transparencia(request):
    f = Subvencion.objects.prefetch_related(
        'likes', 'colectivo', 'responsable', 'se_relaciona_con', 'comments__user', 'comments__subvencion', 'responsable__profile'
    ).select_related(
        'user', 'estado', 'ente', 'area', 'user__profile'
    ).filter(estado_id__in=[5,7,11]).extra(select={"day_mod": "date(fin)"}).order_by('day_mod')

    return render(request,
                  'home/transparencia.html',
                  {'filter' : f})

# --------------- User Registration --------------- #
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("index")

    # if user is logged, redirect him
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('index'))
        return super(RegisterView, self).dispatch(*args, **kwargs)

# --------------- Terms and Privacy --------------- #
def terms_privacy_cookies(request, name):
    template_name = 'home/%s.html' % name
    return render(request,
                  template_name,
                  {})