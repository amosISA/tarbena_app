# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import DetailView

from .models import Profile
from .forms import ProfileForm

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

    def get(self, request, *args, **kwargs):
        """ If user want to access different profile, he will be redirected to his profile """

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if self.request.user.username != self.kwargs.get('username'):
            return(HttpResponseRedirect(reverse('profiles:user_profile', kwargs={'username': self.request.user})))
        else:
            return self.render_to_response(context)

# --------------- Edit User avatar --------------- #
@login_required()
def upload_avatar(request):
    instance = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=instance)

    if request.method == "POST":
        if form.is_valid():
            image_avatar = request.FILES.get('avatar', False)
            instance.avatar = image_avatar
            instance.save()
            return HttpResponseRedirect(reverse('profiles:user_profile', kwargs={'username': request.user}))

    context = {
        "instance": instance,
        "form": form
    }
    return render(request, 'profiles/upload_avatar.html', context)