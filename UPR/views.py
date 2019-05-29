from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Maquina, TipoMaquina, Componentes, Incidencias, MovimientoMaquinaria, Poblacion, GrupoComponentes, RevisionesTemporada, Obra, MantenimientoMaquinaria

# Create your views here.
# --------------- Maquina Index --------------- #
@login_required()
def index_maquinas(request):
    maquinas = Maquina.objects.all()
    return render(request,
                  'UPR/index.html',
                  {'maquinas':maquinas})

# --------------- Maquina Details --------------- #
def maquina_detail(request, ninventario):
    maquina = get_object_or_404(Maquina.objects.select_related(
                                            'tipo_maquina','capataz_responsable','poblacion'
                                        ).prefetch_related('incidencias').order_by('indicencias__fecha'),
                                numero_inventario=ninventario)

    componentes = Componentes.objects.all().filter(tipo_maquina=maquina.tipo_maquina)
    movimientos = MovimientoMaquinaria.objects.all().filter(numero_inventario_mm=maquina.numero_inventario)
    poblacion = Poblacion.objects.all().filter(nombre=maquina.poblacion)
    incidencias = maquina.incidencias.all()
    grupos_componentes = GrupoComponentes.objects.all()
    mantenimiento_maquinaria = MantenimientoMaquinaria.objects.all()


    return render(request,
                  'UPR/detail.html',
                  {'maquina': maquina,
                   'ninventario': ninventario,
                   'componentes': componentes,
                   'movimientos': movimientos,
                   'poblacion': poblacion,
                   'incidencias': incidencias,
                   'grupos_componentes': grupos_componentes,
                   'mantenimiento_maquinaria': mantenimiento_maquinaria,
                   })


# --------------- add_incidencia --------------- #
def add_incidencia(request, ninventario):
    maquina = get_object_or_404(Maquina.objects.select_related(
                                            'tipo_maquina','capataz_responsable','poblacion'
                                        ).prefetch_related('incidencias').order_by('indicencias__fecha'),
                                numero_inventario=ninventario)

    componentes = Componentes.objects.all().filter(tipo_maquina=maquina.tipo_maquina)
    movimientos = MovimientoMaquinaria.objects.all().filter(numero_inventario_mm=maquina.numero_inventario)
    poblacion = Poblacion.objects.all().filter(nombre=maquina.poblacion)
    incidencias = maquina.incidencias.all()
    grupos_componentes = GrupoComponentes.objects.all().order_by('position_grupo_componentes')
    mantenimiento_maquinaria = MantenimientoMaquinaria.objects.all()

    return render(request,
              'UPR/incidencias.html',
              {'maquina': maquina,
               'ninventario': ninventario,
               'componentes': componentes,
               'movimientos': movimientos,
               'poblacion': poblacion,
               'incidencias': incidencias,
               'grupos_componentes': grupos_componentes,
               'mantenimiento_maquinaria': mantenimiento_maquinaria,
               })


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