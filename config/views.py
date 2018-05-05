# -*- coding: utf-8 -*-
from django.contrib.auth.views import login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

# --------------- Index --------------- #
def index(request):
    if request.user.is_authenticated():
        return render(request, 'index.html', {})
    else:
        return login(request, template_name='login.html')

# --------------- Login --------------- #
def custom_login(request, *args, **kwargs):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    else:
        return login(request, template_name='login.html')
    return login(request, *args, **kwargs)