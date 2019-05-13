from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Maquina, TipoMaquina, Componentes, Incidencias

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
                                            'tipo_maquina','capataz_responsable'
                                        ).prefetch_related('incidencias'),
                                numero_inventario=ninventario)

    return render(request,
                  'UPR/detail.html',
                  {'maquina': maquina,
                   'ninventario': ninventario})