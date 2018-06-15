# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView

from .models import Profile

User = get_user_model()

# --------------- User activation email --------------- #
def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = Profile.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            profile = qs.first()
            if not profile.activated:
                user_ = profile.user
                user_.is_active = True
                user_.save()
                profile.activated = True
                profile.activation_key = None
                profile.save()
                return redirect("login")
    # invalid code
    return redirect("login")

# --------------- User Profile Detail View --------------- #
class ProfileDetailView(LoginRequiredMixin ,DetailView):
    queryset = User.objects.filter(is_active=True)
    template_name = 'profiles/profile.html'

    def get_object(self):
        username = self.kwargs.get("username")

        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)