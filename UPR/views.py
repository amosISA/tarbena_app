from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Maquina, TipoMaquina, Componentes, Incidencias, MovimientoMaquinaria, Poblacion

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

    return render(request,
                  'UPR/detail.html',
                  {'maquina': maquina,
                   'ninventario': ninventario,
                   'componentes': componentes,
                   'movimientos': movimientos,
                   'poblacion': poblacion})




