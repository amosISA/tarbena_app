# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup
from django.conf import settings
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import transaction
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.template.loader import render_to_string
from django.utils.module_loading import import_string
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from notify.signals import notify

from .forms import SubvencionForm, CommentFormSet, SubvencionFilter
from .models import Subvencion, Estado, Colectivo, Area, Ente, Comment
from src.config.settings.base import MARTOR_MARKDOWNIFY_FUNCTION

import weasyprint

# --------------- Index: List Subvenciones --------------- #
@login_required()
def index_subvenciones(request, estado_slug=None):
    """ List subvenciones """

    estado, area, user = None, None, None

    # Sidebar filtering
    f = SubvencionFilter(request.GET, queryset=Subvencion.objects.prefetch_related(
            'likes', 'colectivo', 'responsable', 'se_relaciona_con', 'comments__user', 'comments__subvencion'
        ).select_related(
            'user', 'estado', 'ente', 'area'
        ).all())

    # If is superuser: list all subsidies, if not, only the related to the respective user
    if request.user.is_superuser:
        subvenciones = Subvencion.objects.prefetch_related(
            'likes', 'colectivo', 'responsable', 'se_relaciona_con', 'comments__user', 'comments__subvencion'
        ).select_related(
            'user', 'estado', 'ente', 'area'
        ).extra(select={"day_mod": "date(fin)"}).order_by('day_mod')
    else:
        subvenciones = Subvencion.objects.prefetch_related(
            'likes', 'colectivo', 'responsable', 'se_relaciona_con', 'comments__user', 'comments__subvencion'
        ).select_related(
            'user', 'estado', 'ente', 'area'
        ).filter(responsable=request.user)

    total_subvenciones = Subvencion.objects.count()
    colectivos = Colectivo.objects.all()
    userlikes = Subvencion.objects.filter(likes__in=[request.user])

    # Handle user favourites
    if request.path == '/subvenciones/favourites/':
        subvenciones = Subvencion.objects.prefetch_related(
            'likes', 'colectivo', 'responsable', 'se_relaciona_con', 'comments__user', 'comments__subvencion'
        ).select_related(
            'user', 'estado', 'ente', 'area'
        ).filter(likes__in=[request.user])
    else:
        subvenciones = Subvencion.objects.prefetch_related('likes', 'colectivo', 'responsable').all()

    days_until_estado = ['7d', '6d', '5d', '4d', '3d', '2d', '1d', 'expires today', 'expired']

    return render(request,
                  'subvenciones/index.html',
                  {'estado': estado,
                   'area': area,
                   'user': user,
                   'subvenciones': subvenciones,
                   'filter' : f,
                   'days_until_estado': days_until_estado,
                   'total_subvenciones': total_subvenciones,
                   'colectivos': colectivos,
                   'userlikes': userlikes})

# --------------- Get Areas related to each ente with AJAX --------------- #
def ajax_se_relaciona_con(request):
    diputacion = request.GET.getlist('diputacion_ajax[]', '0')
    generalitat = request.GET.getlist('generalitat_ajax[]', '0')
    gobierno = request.GET.getlist('gobierno_ajax[]', '0')

    query = Subvencion.objects.all().filter(Q(area__id__in=diputacion) |
                                      Q(area__id__in=generalitat) |
                                      Q(area__id__in=gobierno))
    data = serializers.serialize('json', query)
    return HttpResponse(data, content_type="application/json")

def subsidies_for_ajax_loop(request):
    subvenciones = Subvencion.objects.all()
    diputacion = Area.objects.filter(ente_id=1)
    generalitat = Area.objects.filter(ente_id=2)
    gobierno = Area.objects.filter(ente_id=3)

    return render(request,
                  'subvenciones/ajax_se_relaciona_con_modal.html',
                  {'subvenciones':subvenciones,
                   'diputacion':diputacion,
                   'generalitat':generalitat,
                   'gobierno':gobierno})

# --------------- Likes --------------- #
@login_required
@require_POST
def likes(request):
    subsidie_id = request.POST.get('id')
    action = request.POST.get('action')

    if subsidie_id and action:
        try:
            subsidie = Subvencion.objects.get(id=subsidie_id)
            if action == 'like':
                subsidie.likes.add(request.user)
            else:
                subsidie.likes.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
        return JsonResponse({'status':'ko'})

# --------------- Create New Subsidie --------------- #
class SubvencionCreateView(LoginRequiredMixin, CreateView):
    form_class = SubvencionForm
    template_name = 'subvenciones/create.html'
    success_url = reverse_lazy('subvenciones:index')

    def get_initial(self):
        super(SubvencionCreateView, self).get_initial()
        user = self.request.user
        self.initial = {"estado": 4, "user": user.id, "colectivo": 1}
        return self.initial

    def get(self, request, *args, **kwargs):
        """Primero ponemos nuestro object como nulo, se debe tener en
        cuenta que object se usa en la clase CreateView para crear el objeto"""
        self.object = None
        # Instanciamos el formulario de la Subvención que declaramos en la variable form_class
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # Instanciamos el formset con un valor inicial
        comments_formset = CommentFormSet(initial=[{'user':request.user}])
        # Renderizamos el formulario de la Subvención y el formset
        return self.render_to_response(self.get_context_data(form=form,
                                                             comments_formset=comments_formset))

    def post(self, request, *args, **kwargs):
        # Obtenemos nuevamente la instancia del formulario de Subvención
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # Obtenemos el formset pero ya con lo que se le pasa en el POST
        comments_formset = CommentFormSet(request.POST)
        """Llamamos a los métodos para validar el formulario de Subvención y el formset, si son válidos ambos se llama al método
        form_valid o en caso contrario se llama al método form_invalid"""
        if form.is_valid() and comments_formset.is_valid():
            return self.form_valid(form, comments_formset)
        else:
            return self.form_invalid(form, comments_formset)

    def form_valid(self, form, comments_formset):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object = form.save()
        comments_formset.instance = self.object

        comments_formset.save(commit=False)
        for f in comments_formset:
            contenido = f.cleaned_data.get("contenido")
            if contenido:
                # Notify and email comment
                location = reverse("subvenciones:subvencion_detail", kwargs={'id': self.object.pk})
                url = self.request.build_absolute_uri(location)
                markdown_find_mentions(self.request.POST['comments-0-contenido'],
                                       self.request.user,
                                       self.request.user.username,
                                       self.object.nombre,
                                       self.request.user.email,
                                       self.object,
                                       url)

        comments_formset.save()

        # If comments are saved without content, they are deleted
        for comment in Comment.objects.all():
            if not comment.contenido:
                comment.delete()

        # Notify
        users = User.objects.all()
        notify.send(self.request.user, recipient_list=list(users), actor=self.request.user,
                    verb='subvención', obj=self.object, target=self.object,
                    nf_type='create_subvencion')

        messages.success(self.request, 'Subvención añadida correctamente!')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, comments_formset):
        # Si es inválido el form de Subvención o el formset renderizamos los errores
        messages.error(self.request, 'Error en la creación de la subvención')
        return self.render_to_response(self.get_context_data(form=form,
                                                             comments_formset=comments_formset))

# --------------- Edit Subsidie --------------- #
class SubvencionUpdateView(LoginRequiredMixin, UpdateView):
    model = Subvencion
    form_class = SubvencionForm
    template_name = 'subvenciones/edit.html'
    success_url = reverse_lazy('subvenciones:index')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        comments_formset = CommentFormSet(initial=[{'user':request.user}])

        return self.render_to_response(self.get_context_data(form=form,
                                                             comments_formset=comments_formset))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        comments_formset = CommentFormSet(request.POST)

        if form.is_valid() and comments_formset.is_valid():
            return self.form_valid(form, comments_formset)
        else:
            return self.form_invalid(form, comments_formset)

    def form_valid(self, form, comments_formset):
        self.object = form.save()
        comments_formset.instance = self.object

        comments_formset.save(commit=False)
        for f in comments_formset:
            contenido = f.cleaned_data.get("contenido")
            if contenido:
                # Notify and email comment
                location = reverse("subvenciones:subvencion_detail", kwargs={'id':self.object.pk})
                url = self.request.build_absolute_uri(location)
                markdown_find_mentions(self.request.POST['comments-0-contenido'],
                                       self.request.user,
                                       self.request.user.username,
                                       self.object.nombre,
                                       self.request.user.email,
                                       self.object,
                                       url)

        comments_formset.save()

        # If comments are saved without content, they are deleted
        for comment in Comment.objects.all():
            if not comment.contenido:
                comment.delete()

        # Notify update subvencion
        users = User.objects.all()
        notify.send(self.request.user, recipient_list=list(users), actor=self.request.user,
                    verb='subvención', obj=self.object, target=self.object,
                    nf_type='edit_subvencion')

        messages.success(self.request, 'Subvención actualizada correctamente!')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, comments_formset):
        messages.error(self.request, 'Error en la actualización de la subvención')
        return self.render_to_response(self.get_context_data(form=form,
                                                             comments_formset=comments_formset))

def markdown_find_mentions(markdown_text, user, user_username, name_subv, mail, object, url):
    """
    To find the users that mentioned
    on markdown content using `BeautifulShoup`.

    Also send email to users that have been mentioned.

    input  : `markdown_text` or markdown content.
    return : `list` of usernames.
    """
    markdownify = import_string(MARTOR_MARKDOWNIFY_FUNCTION)
    mark = markdownify(markdown_text)
    soup = BeautifulSoup(mark, 'html.parser')
    markdown_users = list(set(
        username.text[1::] for username in
        soup.findAll('a', {'class': 'direct-mention-link'})
    ))

    all_users = User.objects.all()
    notify_list_users = []
    email_list_users = []
    for a in all_users:
        if a.username in markdown_users:
            for o in User.objects.all().filter(username=a):
                notify_list_users.append(o)

                if o.email:
                    email_list_users.append(o.email)

    html_message = loader.render_to_string(
        'subvenciones/subv_email_create.html',
        {
            'name_actor': user_username,
            'name_subv': name_subv,
            'object': object,
            'url': url
        }
    )

    send_mail('Gestión de subvenciones',
              '',
              mail,
              email_list_users,  # recievers
              html_message=html_message
    )

    if markdown_users:
        return notify.send(user, recipient_list=list(notify_list_users), actor=user,
                    verb='comentarios', obj=object, target=object,
                    nf_type='mention')
    else:
        return

@login_required()
# --------------- Subsidie Details --------------- #
def subvencion_detail(request, id):
    subvencion = get_object_or_404(Subvencion.objects.prefetch_related(
                                                        'likes', 'colectivo', 'responsable', 'se_relaciona_con', 'comments__user', 'comments__subvencion'
                                                    ).select_related(
                                                        'user', 'estado', 'ente', 'area'
                                                    ),
                                   id=id)
    diputacion = Subvencion.objects.filter(se_relaciona_con=subvencion, ente__id=1)
    generalitat = Subvencion.objects.filter(se_relaciona_con=subvencion, ente__id=2)
    gobierno = Subvencion.objects.filter(se_relaciona_con=subvencion, ente__id=3)

    return render(request,
                  'subvenciones/detail.html',
                  {'subvencion': subvencion,
                   'diputacion': diputacion,
                   'generalitat': generalitat,
                   'gobierno': gobierno})

# --------------- Delete Subsidie --------------- #
class SubvencionDeleteView(LoginRequiredMixin, DeleteView):
    model = Subvencion
    success_url = reverse_lazy('subvenciones:index')

    def get_object(self, queryset=None):
        obj = super(SubvencionDeleteView, self).get_object()
        return obj

    def post(self, request, *args, **kwargs):
        if self.request.POST.get("confirm_delete"):
            # Notify
            users = User.objects.all()
            notify.send(self.request.user, recipient_list=list(users), actor=self.request.user,
                        verb='subvención, %s' % (self.get_object()), nf_type='delete_subvencion')

            # when confirmation page has been displayed and confirm button pressed
            self.get_object().delete()
            messages.success(self.request, 'Subvención eliminada correctamente!')
            return HttpResponseRedirect(self.success_url)
        elif self.request.POST.get("cancel"):
            # when confirmation page has been displayed and cancel button pressed
            return HttpResponseRedirect(reverse('subvenciones:index'))
        else:
            # when data is coming from the form which lists all items
            return self.get(self, *args, **kwargs)

# --------------- PDF Detail Subsidie --------------- #
@login_required()
def admin_subvencion_pdf(request, subvencion_id):
    subvencion = get_object_or_404(Subvencion, id=subvencion_id)
    html = render_to_string('subvenciones/pdf_detail.html',
                            {'subvencion': subvencion})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=subvencion_{}.pdf'.format(subvencion.id)
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(
                                               settings.STATIC_ROOT + '/subvenciones/css/pdf.css'
                                           )])
    return response