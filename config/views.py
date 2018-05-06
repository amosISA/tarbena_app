# -*- coding: utf-8 -*-
from django.contrib.auth.views import login
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView

from .forms import RegisterForm

# --------------- Index --------------- #
def index(request):
    if request.user.is_authenticated():
        return render(request, 'home/index.html', {})
    else:
        return HttpResponseRedirect(reverse('login'))

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