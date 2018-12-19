# -*- coding: utf-8 -*-
from django.core import serializers
from django.core.urlresolvers import reverse_lazy
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .models import Parcela, Proyecto, SectorTrabajo, Poblacion, Propietario
from .forms import ParcelaForm

from bs4 import BeautifulSoup
from dal import autocomplete
from weasyprint import HTML

import datetime
import urllib.request
import weasyprint

@permission_required('parcelas.can_add_parcela', raise_exception=True)
def index(request):
    parcelas = Parcela.objects.all()
    proyectos = Proyecto.objects.all()
    poblacion = Poblacion.objects.all()

    return render(request,
                  'parcelas/index.html',
                  {'parcelas': parcelas,
                   'proyectos': proyectos,
                   'poblacion': poblacion})

def ajax_get_parcelas(request):
    sector = request.GET.get('sector-name', '99999')

    # get sectores that belong to a project
    # antes de cambiarlo a manytomany en parcelas para sectores, estaba así sin quitar el manytomany en sectores
    # query = Parcela.objects.all().filter(sectortrabajo=sector)
    query = Parcela.objects.all().prefetch_related(
            'sector_trabajo'
        ).select_related(
            'propietario', 'poblacion', 'estado', 'estado_parcela_trabajo'
        ).filter(sector_trabajo=sector)
    data = serializers.serialize('json', query, indent=2,
                                 use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return HttpResponse(data, content_type="application/json")

def ajax_get_sectores(request):
    proyecto = request.GET.get('project_name', '99999')

    # get sectores that belong to a project
    query = SectorTrabajo.objects.all().filter(proyecto=proyecto)
    data = serializers.serialize('json', query)
    return HttpResponse(data, content_type="application/json")

def ajax_get_projects(request):
    query = Proyecto.objects.all()
    data = serializers.serialize('json', query)
    return HttpResponse(data, content_type="application/json")

# class DetailPropietarioParcela(DetailView):
#     model = Propietario
#     template_name = 'parcelas/propietario_detail.html'

# --------------- Create New Parcela --------------- #
class ParcelaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('subvenciones.can_add_parcela')
    raise_exception = True
    form_class = ParcelaForm
    template_name = 'parcelas/parcela_create.html'
    success_url = reverse_lazy('parcelas:index')

    def form_valid(self, form):
        print(self.object)
        return super(ParcelaCreateView, self).form_valid(form)

@permission_required('parcelas.can_add_parcela', raise_exception=True)
def ParcelaCreate(request):
    data = dict()

    if request.method == 'POST':
        form = ParcelaForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = ParcelaForm()

    context = {'form': form}
    data['html_form'] = render_to_string('parcelas/parcela_create.html',
                                         context,
                                         request=request
                                         )
    return JsonResponse(data)

# @permission_required('parcelas.can_add_parcela', raise_exception=True)
class PropietarioAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Propietario.objects.all()

        if self.q:
            qs = qs.filter(
                Q(nombre__icontains=self.q) |
                Q(nombre__iexact=self.q) |
                Q(apellidos__icontains=self.q) |
                Q(apellidos__iexact=self.q) |
                Q(apellidos2__icontains=self.q) |
                Q(apellidos2__iexact=self.q) |
                Q(nif__icontains=self.q) |
                Q(nif__iexact=self.q) |
                Q(direccion__icontains=self.q) |
                Q(direccion__iexact=self.q) |
                Q(telefono_movil__icontains=self.q) |
                Q(telefono_movil__iexact=self.q) |
                Q(telefono_fijo__icontains=self.q) |
                Q(telefono_fijo__iexact=self.q) |
                Q(email__icontains=self.q) |
                Q(email__iexact=self.q) |
                Q(comentarios__icontains=self.q) |
                Q(comentarios__iexact=self.q)
            )

        return qs

# Ajax for gettings m2 from url with b4
def get_m2_url(request):
    poblacion = request.GET.get('poblacion', '127')
    poligono = request.GET.get('poligono', '10')
    parcela = request.GET.get('parcela', '99999')

    my_url = "https://www1.sedecatastro.gob.es/CYCBienInmueble/OVCConCiud.aspx?del=3&mun=" + poblacion + "&UrbRus=&RefC=03" + poblacion + "A" + poligono + parcela + "0000BL&Apenom=&esBice=&RCBice1=&RCBice2=&DenoBice=&latitud=&longitud=&gradoslat=&minlat=&seglat=&gradoslon=&minlon=&seglon=&x=&y=&huso=&tipoCoordenadas="
    uClient = urllib.request.urlopen(my_url)
    page_html = uClient.read()
    uClient.close()

    page_soup = BeautifulSoup(page_html, "html.parser")

    labels = page_soup.findAll("sup")

    data = ''
    for l in labels:
        x = l.previous_sibling.split('m')
        data = data + x[0]
        break

    return JsonResponse(data, safe=False)

def autorization_pdf_maker(request, parcela_id):
    now = datetime.datetime.now()
    parcela = get_object_or_404(Parcela, id=parcela_id)
    html = render_to_string('parcelas/pdf_autorizacion.html',
                            {'parcela': parcela,
                             'now': now})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=parcela_{}.pdf'.format(parcela.id)
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)
    return response

def get_propietario_parcelas(request):
    id_propietario = request.GET.get('id_propietario', '999999')
    parcelas_prop = Parcela.objects.all().prefetch_related(
            'sector_trabajo'
        ).select_related(
            'propietario', 'poblacion', 'estado', 'estado_parcela_trabajo'
        ).filter(propietario_id=id_propietario)

    data = serializers.serialize('json', parcelas_prop)
    return HttpResponse(data, content_type="application/json")