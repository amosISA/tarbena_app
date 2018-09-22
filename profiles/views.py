# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files import File
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView

from .models import Profile
from .forms import ProfileForm
from PIL import Image
from io import BytesIO

import io

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
class ProfileDetailView(LoginRequiredMixin, DetailView):
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

# --------------- Update User Information --------------- #
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'profiles/update_profile.html'
    fields = ['username', 'email', 'first_name', 'last_name']

    def get_success_url(self):
        return reverse('profiles:user_profile', kwargs={'username': self.request.user})

    def get_object(self, queryset=None):
        """
        This method will load the object
        that will be used to load the form
        that will be edited
        """

        return self.request.user

# --------------- Edit User avatar --------------- #
@login_required()
def upload_avatar(request):
    instance = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=instance)

    if request.method == "POST":
        if form.is_valid():
            image_avatar = request.FILES.get('avatar', False)

            # Change image size
            im = Image.open(image_avatar)
            output = BytesIO()
            im = im.resize((100, 100))
            im = im.convert("RGB") # to avoid: cannot write mode RGBA as JPEG
            im.save(output, format='JPEG', quality=100)

            instance.avatar = image_avatar
            instance.save()
            return HttpResponseRedirect(reverse('profiles:user_profile', kwargs={'username': request.user}))

    context = {
        "instance": instance,
        "form": form
    }
    return render(request, 'profiles/upload_avatar.html', context)

# --------------- User Change Password --------------- #
@login_required()
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Su contraseña se ha actualizado correctamente!')
            return HttpResponseRedirect(reverse('profiles:user_profile', kwargs={'username': request.user}))
        else:
            messages.error(request, 'Ha ocurrido un error al cambiar la contraseña.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {
        'form': form
    })