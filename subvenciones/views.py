# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import transaction
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import SubvencionForm, CommentFormSet
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
            subvenciones = subvenciones.filter(area__nombre=area)
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
        # Aquí ya guardamos el object de acuerdo a los valores del formulario de Subvención
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object = form.save()
        # Utilizamos el atributo instance del formset para asignarle el valor del objeto Subvención creado y que nos indica el modelo Foráneo
        # Es decir, al model Comment se le relaciona la subvención
        comments_formset.instance = self.object
        # Finalmente guardamos el formset para que tome los valores que tiene
        comments_formset.save()
        # Redireccionamos a la ventana del listado de subvenciones con el mensaje de éxito
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
        comments_formset.save()
        messages.success(self.request, 'Subvención actualizada correctamente!')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, comments_formset):
        messages.error(self.request, 'Error en la actualización de la subvención')
        return self.render_to_response(self.get_context_data(form=form,
                                                             comments_formset=comments_formset))

@login_required()
# --------------- Subsidie Details --------------- #
def subvencion_detail(request, id):
    subvencion = get_object_or_404(Subvencion,
                                   id=id)

    return render(request,
                  'subvenciones/detail.html',
                  {'subvencion': subvencion})

# --------------- Delete Subsidie --------------- #
class SubvencionDeleteView(LoginRequiredMixin, DeleteView):
    model = Subvencion
    success_url = reverse_lazy('subvenciones:index')

    def get_object(self, queryset=None):
        obj = super(SubvencionDeleteView, self).get_object()
        return obj

    def post(self, request, *args, **kwargs):
        if self.request.POST.get("confirm_delete"):
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