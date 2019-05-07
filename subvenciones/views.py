# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup
from datetime import *
from django.conf import settings
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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
from .tasks import subvencion_mention_email, subvencion_create_email, subvencion_edit_email, subvencion_responsable_email
# from src.config.settings.base import MARTOR_MARKDOWNIFY_FUNCTION

import weasyprint
import xlwt

import sys
sys.path.append("..")
from profiles.models import Profile

# --------------- Index: List Subvenciones --------------- #
@login_required()
@permission_required('subvenciones.add_subvencion', raise_exception=True)
def index_subvenciones(request, estado_slug=None):
    """ List subvenciones """

    area = None
    estado = None
    profile = None

    total_subvenciones = Subvencion.objects.count()
    colectivos = Colectivo.objects.all()
    userlikes = Subvencion.objects.filter(likes__in=[request.user])
    days_until_estado = ['7d', '6d', '5d', '4d', '3d', '2d', '1d', 'expires today', 'expired']
    estados = Estado.objects.all().annotate(the_count=Count('subvencion__estado')) # later in template i can use: e.the_count

    # Handle user favourites
    if request.path == '/subvenciones/favourites/':
        f = SubvencionFilter(request.GET, queryset=Subvencion.objects.prefetch_related(
            'likes', 'colectivo', 'responsable', 'se_relaciona_con', 'comments__user', 'comments__subvencion', 'responsable__profile'
        ).select_related(
            'user', 'estado', 'ente', 'area', 'user__profile'
        ).filter(likes__in=[request.user]))
    else:
        # If is superuser: list all subsidies, if not, only the related to the respective user
        if request.user.is_superuser:
            request.session['urltoremember'] = request.get_full_path()
            request.session.set_expiry(604800)
            f = SubvencionFilter(request.GET, queryset=Subvencion.objects.prefetch_related(
                'likes', 'colectivo', 'responsable', 'se_relaciona_con', 'comments__user', 'comments__subvencion', 'responsable__profile'
            ).select_related(
                'user', 'estado', 'ente', 'area', 'user__profile'
            ).extra(select={"day_mod": "date(fin)"}).order_by('day_mod'))
        else:
            request.session['urltoremember'] = request.get_full_path()
            request.session.set_expiry(604800)
            f = SubvencionFilter(request.GET, queryset=Subvencion.objects.prefetch_related(
                'likes', 'colectivo', 'responsable', 'se_relaciona_con', 'comments__user', 'comments__subvencion', 'responsable__profile'
            ).select_related(
                'user', 'estado', 'ente', 'area', 'user__profile'
            ).filter(responsable=request.user))

    if estado_slug:
        if Area.objects.filter(slug=estado_slug).exists():
            area = get_object_or_404(Area, slug=estado_slug)
            f = SubvencionFilter(request.GET, queryset=Subvencion.objects.prefetch_related(
                'likes', 'colectivo', 'responsable', 'se_relaciona_con', 'comments__user', 'comments__subvencion',
                'responsable__profile'
            ).select_related(
                'user', 'estado', 'ente', 'area', 'user__profile'
            ).filter(area=area))
        elif Estado.objects.filter(slug=estado_slug).exists():
            estado = get_object_or_404(Estado, slug=estado_slug)
            f = SubvencionFilter(request.GET, queryset=Subvencion.objects.prefetch_related(
                'likes', 'colectivo', 'responsable', 'se_relaciona_con', 'comments__user', 'comments__subvencion',
                'responsable__profile'
            ).select_related(
                'user', 'estado', 'ente', 'area', 'user__profile'
            ).filter(estado=estado))
        # elif Profile.objects.filter(slug=estado_slug).exists():
        #     profile = get_object_or_404(Profile, slug=estado_slug)
        #     f = SubvencionFilter(request.GET, queryset=Subvencion.objects.prefetch_related(
        #         'likes', 'colectivo', 'responsable', 'se_relaciona_con', 'comments__user', 'comments__subvencion',
        #         'responsable__profile'
        #     ).select_related(
        #         'user', 'estado', 'ente', 'area', 'user__profile'
        #     ).filter(responsable__profile=profile))

    return render(request,
                  'subvenciones/index.html',
                  {'filter' : f,
                   'days_until_estado': days_until_estado,
                   'total_subvenciones': total_subvenciones,
                   'colectivos': colectivos,
                   'userlikes': userlikes,
                   'estados': estados,
                   'urltoremember': request.session.get('urltoremember', None),
                   'area': area,
                   'estado': estado,
                   'profile': profile})

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
class SubvencionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('subvenciones.add_subvencion')
    raise_exception = True
    form_class = SubvencionForm
    template_name = 'subvenciones/create.html'

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
            else:
                # Email that someone has created subsidie
                location = reverse("subvenciones:subvencion_detail", kwargs={'id': self.object.pk})
                url = self.request.build_absolute_uri(location)

                # launch asynchronous task - celery
                subvencion_create_email.delay(self.request.user.username, self.object.nombre, self.object, url,
                                            self.request.user.email, ['amosisa700@gmail.com', 'jctarbena@gmail.com'])

        # send asynchronous task - celery when Subvencion is assigned to Users
        assigned_responsables = form.cleaned_data.get("responsable")
        if assigned_responsables:
            resp_list = []
            for r in assigned_responsables:
                resp_list.append(r.email)

                subvencion_responsable_email.delay(self.request.user.username, self.object.nombre, self.object,
                                                   self.request.build_absolute_uri(
                                                       reverse("subvenciones:subvencion_detail",
                                                               kwargs={'id': self.object.pk})),
                                                   self.request.user.email, resp_list)

        comments_formset.save()

        # If comments are saved without content, they are deleted
        for comment in Comment.objects.all():
            if not comment.contenido:
                comment.delete()

        # Notify
        users = User.objects.filter(Q(groups__name='staff') | Q(is_staff=True)).distinct()
        notify.send(self.request.user, recipient_list=list(users), actor=self.request.user,
                    verb='subvención', obj=self.object, target=self.object,
                    nf_type='create_subvencion')

        messages.success(self.request, 'Subvención añadida correctamente!')
        return HttpResponseRedirect(reverse_lazy('subvenciones:subvencion_detail', kwargs={'id': self.object.pk}))

    def form_invalid(self, form, comments_formset):
        # Si es inválido el form de Subvención o el formset renderizamos los errores
        messages.error(self.request, 'Error en la creación de la subvención')
        return self.render_to_response(self.get_context_data(form=form,
                                                             comments_formset=comments_formset))

    def get_context_data(self, **kwargs):
        # Context to remember the index url if someone filter
        context = super(SubvencionCreateView, self).get_context_data(**kwargs)
        context['urltoremember'] = self.request.session.get('urltoremember', None)
        return context

# --------------- Edit Subsidie --------------- #
class SubvencionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('subvenciones.add_subvencion')
    raise_exception = True
    model = Subvencion
    form_class = SubvencionForm
    template_name = 'subvenciones/edit.html'

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
        # Get responsables pre_save
        resp_list_before = []
        before_responsable = self.get_initial_responsables()

        for r in before_responsable:
            resp_list_before.append(r.email)

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
            else:
                # Email that someone has edited subsidie
                location = reverse("subvenciones:subvencion_detail", kwargs={'id': self.object.pk})
                url = self.request.build_absolute_uri(location)

                # launch asynchronous task - celery
                subvencion_edit_email.delay(self.request.user.username, self.object.nombre, self.object, url,
                                            self.request.user.email, ['amosisa700@gmail.com', 'jctarbena@gmail.com'])

        # send asynchronous task - celery when Subvencion is assigned to Users
        resp_list = []
        assigned_responsables = form.cleaned_data['responsable']

        if assigned_responsables:
            for r in assigned_responsables:
                resp_list.append(r.email)

            assigned_resp_def = [item for item in resp_list if item not in resp_list_before]
            if assigned_resp_def:
                subvencion_responsable_email.delay(self.request.user.username, self.object.nombre, self.object,
                                                   self.request.build_absolute_uri(reverse("subvenciones:subvencion_detail", kwargs={'id':self.object.pk})),
                                                   self.request.user.email, assigned_resp_def)

        comments_formset.save()

        # If comments are saved without content, they are deleted
        for comment in Comment.objects.all():
            if not comment.contenido:
                comment.delete()

        # Notify update subvencion
        users = User.objects.filter(Q(groups__name='staff') | Q(is_staff=True)).distinct()
        notify.send(self.request.user, recipient_list=list(users), actor=self.request.user,
                    verb='subvención', obj=self.object, target=self.object,
                    nf_type='edit_subvencion')

        messages.success(self.request, 'Subvención actualizada correctamente!')
        return HttpResponseRedirect(reverse_lazy('subvenciones:subvencion_detail', kwargs={'id': self.object.pk}))

    def get_initial_responsables(self):
        assigned_responsables = Subvencion.objects.get(id=self.object.pk)
        return assigned_responsables.responsable.all()

    def form_invalid(self, form, comments_formset):
        messages.error(self.request, 'Error en la actualización de la subvención')
        return self.render_to_response(self.get_context_data(form=form,
                                                             comments_formset=comments_formset))

    def get_context_data(self, **kwargs):
        # Context to remember the index url if someone filter
        context = super(SubvencionUpdateView, self).get_context_data(**kwargs)
        context['urltoremember'] = self.request.session.get('urltoremember', None)
        return context

def markdown_find_mentions(markdown_text, user, user_username, name_subv, mail, object, url):
    """
    To find the users that mentioned
    on markdown content using `BeautifulShoup`.

    Also send email to users that have been mentioned.

    input  : `markdown_text` or markdown content.
    return : `list` of usernames.
    """
    markdownify = import_string(getattr(settings, 'MARTOR_MARKDOWNIFY_FUNCTION', None))
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

    # launch asynchronous task - celery
    subvencion_mention_email.delay(user_username, name_subv, object, url, mail, email_list_users)

    if markdown_users:
        return notify.send(user, recipient_list=list(notify_list_users), actor=user,
                    verb='comentarios', obj=object, target=object,
                    nf_type='mention')
    else:
        return

@login_required()
@permission_required('subvenciones.add_subvencion', raise_exception=True)
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
                   'gobierno': gobierno,
                   'urltoremember': request.session.get('urltoremember', None)})

# --------------- Delete Subsidie --------------- #
class SubvencionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('subvenciones.add_subvencion')
    raise_exception = True
    model = Subvencion
    success_url = reverse_lazy('subvenciones:index')

    def get_object(self, queryset=None):
        obj = super(SubvencionDeleteView, self).get_object()
        return obj

    def post(self, request, *args, **kwargs):
        if self.request.POST.get("confirm_delete"):
            # Notify
            users = User.objects.filter(Q(groups__name='staff') | Q(is_staff=True)).distinct()
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

    def get_context_data(self, **kwargs):
        # Context to remember the index url if someone filter
        context = super(SubvencionDeleteView, self).get_context_data(**kwargs)
        context['urltoremember'] = self.request.session.get('urltoremember', None)
        return context

# --------------- PDF Detail Subsidie --------------- #
@login_required()
@permission_required('subvenciones.add_subvencion', raise_exception=True)
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

# --------------- EXPORT TO EXCEL --------------- #
import re
@login_required
@permission_required('subvenciones.add_subvencion', raise_exception=True)
def export_subvenciones_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="subvenciones.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Subvenciones')

    # Sheet header, first row
    row_num = 0

    columns = [
        ('G: Cód Gasto', 4000), ('G: Desc Gasto', 12000), ('G: Año', 4000),
        ('G: Coeficiente Financiación', 2000), ('G: Aplic Presupuestaria', 5000),
        ('I: Admón Que Financia', 4000), ('I: Año', 3000), ('I: Importe', 5000),
        ('I: Aplic Presupuestaria', 5000)
    ]

    font_style = xlwt.easyxf('align: wrap yes,vert centre, horiz center;pattern: pattern solid, \
                                       fore-colour light_blue ;border: left medium,right medium,top medium,bottom medium')
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    # Sheet body, remaining rows
    font_style = xlwt.easyxf(
        'align: wrap on,vert center, horiz left;border: left thin,right thin,top thin,bottom thin')

    # Subvenciones with estado_id: 5, 7 and 11
    rows = Subvencion.objects.all().filter(estado_id__in=[5,7,11]).values_list('impreso', 'nombre', 'cuantia_inicial', 'impreso',
                                                                                'impreso', 'ente__nombre'.split(' ')[0], 'impreso',
                                                                                'cuantia_inicial', 'impreso')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 5:
                ws.write(row_num, col_num, row[col_num].split(' ')[0], font_style)
            elif col_num == 2 or col_num == 7:
                ws.write(row_num, col_num, re.sub("\D", "", str(row[col_num])), font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)

    row_num += 3
    font_style = xlwt.easyxf('align: wrap yes,vert centre, horiz center \
                                           ;border: left thin,right thin,top thin,bottom thin')
    ws.write(row_num, 0, 'ESTADO DEFINIÉNDOSE', font_style)

    # Subvenciones with estado_id: 4
    rows_def = Subvencion.objects.all().filter(estado_id=4).values_list('impreso', 'nombre', 'cuantia_inicial',
                                                                                 'impreso',
                                                                                 'impreso', 'ente__nombre', 'impreso',
                                                                                 'cuantia_inicial',
                                                                                 'impreso')

    font_style = xlwt.easyxf('align: wrap yes,vert centre, horiz left \
                                               ;border: left thin,right thin,top thin,bottom thin')

    for row in rows_def:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 5:
                ws.write(row_num, col_num, row[col_num].split(' ')[0], font_style)
            elif col_num == 2 or col_num == 7:
                ws.write(row_num, col_num, re.sub("\D", "", str(row[col_num])), font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

# --------------- Ajax Reset Filtering Button --------------- #
@login_required
def reset_filtering_button(request):
    if 'urltoremember' in request.session:
        del request.session['urltoremember']
        filter='¡Filtro reiniciado!'
    else:
        filter='No'
    data = {
        'filter': filter
    }
    return JsonResponse(data)

# --------------- Subvenciones that expires in the next 5 days (their fin field) --------------- #
def subvenciones_expires_next_five_days(request):
    ls = []
    subvenciones = Subvencion.objects.prefetch_related(
            'likes', 'colectivo', 'responsable', 'se_relaciona_con', 'comments__user', 'comments__subvencion', 'responsable__profile'
        ).select_related(
            'user', 'estado', 'ente', 'area', 'user__profile'
        )

    today = date.today()
    for s in subvenciones:
        if s.fin:
            if s.fin > today:
                ls.append(s)

    return render(request,
                  'subvenciones/expiration.html',
                  {'subvenciones': ls,
                   'today': today})