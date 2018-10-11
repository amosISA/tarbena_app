# -*- coding: utf-8 -*-
from django.core import serializers
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .models import Parcela, Proyecto, SectorTrabajo, Propietario, Poblacion
from .forms import ParcelaForm

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
    query = Parcela.objects.all().filter(sector_trabajo=sector)
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

class DetailPropietarioParcela(DetailView):
    model = Propietario
    template_name = 'parcelas/propietario_detail.html'

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