from django.contrib import messages
from django.core import serializers
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView

from .models import Maquina, TipoMaquina, Componentes, Incidencias, MovimientoMaquinaria, Poblacion, GrupoComponentes, RevisionesTemporada, Obra, MantenimientoMaquinaria, MovimientoObra
from .forms import MaquinaIncidenciasForm, MovimientoMaquinariaForm, MovimientoObraForm

# Create your views here.

# --------------- Maquina Index --------------- #
@login_required()
def index_maquinas(request):
    maquinas = Maquina.objects.filter(capataz_responsable=request.user.id).all()
    poblacion = MovimientoMaquinaria.objects.all()[:1]
    desbro = Maquina.objects.filter(tipo_maquina='3').order_by('fecha_compra')
    moto261 = Maquina.objects.filter(tipo_maquina='5')
    moto241 = Maquina.objects.filter(tipo_maquina='4')
    moto101 = Maquina.objects.filter(tipo_maquina='1')
    moto103 = Maquina.objects.filter(tipo_maquina='2')
    #número de máquinas según su tipo
    numMaquina = Maquina.objects.count()
    numDesbro = Maquina.objects.filter(tipo_maquina='3').count()
    numMoto261 = Maquina.objects.filter(tipo_maquina='5').count()
    numMoto241 = Maquina.objects.filter(tipo_maquina='4').count()
    numMoto101 = Maquina.objects.filter(tipo_maquina='1').count()
    numMoto103 = Maquina.objects.filter(tipo_maquina='2').count()
    #mostramos las máquinas pertenecientes a la obra 0748241
    #también mostramos cada tipo de máquina de esta obra
    numMaquinaObra0748241 = Maquina.objects.filter(obra__nombre_obra__exact='1').count()
    numDesbro_0748241 = Maquina.objects.filter(obra__nombre_obra__exact='1').filter(tipo_maquina='3').count()
    numMoto241_0748241 = Maquina.objects.filter(obra__nombre_obra__exact='1').filter(tipo_maquina='4').count()
    numMoto261_0748241 = Maquina.objects.filter(obra__nombre_obra__exact='1').filter(tipo_maquina='5').count()
    numMoto101_0748241 = Maquina.objects.filter(obra__nombre_obra__exact='1').filter(tipo_maquina='1').count()
    numMoto103_0748241 = Maquina.objects.filter(obra__nombre_obra__exact='1').filter(tipo_maquina='2').count()


    cerrado = Maquina.objects.filter(incidencias__cerrado=False)


    # movimientos = Maquina.maquina_poblacion.poblacion_mm.order_by('-fecha_movimiento')[0]
    llegandoCerrado = Maquina.objects.select_related(
        'tipo_maquina', 'capataz_responsable',
    ).prefetch_related('incidencias')
    return render(request,
                  'UPR/index.html',
                  {'maquinas':maquinas,
                   'desbro':desbro,
                   'moto261':moto261,
                   'moto241': moto241,
                   'moto101': moto101,
                   'moto103': moto103,
                   'llegandoCerrado':llegandoCerrado,
                   'numMaquina':numMaquina,
                   'numMaquinaObra0748241':numMaquinaObra0748241,
                   'numDesbro': numDesbro,
                   'numMoto261':numMoto261,
                   'numMoto241':numMoto241,
                   'numMoto101':numMoto101,
                   'numMoto103':numMoto103,
                   'numDesbro_0748241': numDesbro_0748241,
                   'numMoto241_0748241': numMoto241_0748241,
                   'numMoto261_0748241': numMoto261_0748241,
                   'numMoto101_0748241': numMoto101_0748241,
                   'numMoto103_0748241': numMoto103_0748241,
                   'cerrado' : cerrado,
                   'poblacion' : poblacion,
                   })






# --------------- inventario maquinas --------------- #
@login_required()
def inventario_maquinas(request):
    maquinas = Maquina.objects.filter(capataz_responsable=request.user.id).all()
    poblacion = MovimientoMaquinaria.objects.all()[:1]
    desbro = Maquina.objects.filter(tipo_maquina='3').order_by('fecha_compra')
    #desbro = Maquina.objects.prefetch_related('obra').order_by('-fecha_compra')

    moto261 = Maquina.objects.filter(tipo_maquina='5')
    moto241 = Maquina.objects.filter(tipo_maquina='4')
    moto101 = Maquina.objects.filter(tipo_maquina='1')
    moto103 = Maquina.objects.filter(tipo_maquina='2')
    # número de máquinas según su tipo
    numMaquina = Maquina.objects.count()
    numDesbro = Maquina.objects.filter(tipo_maquina='3').count()
    numMoto261 = Maquina.objects.filter(tipo_maquina='5').count()
    numMoto241 = Maquina.objects.filter(tipo_maquina='4').count()
    numMoto101 = Maquina.objects.filter(tipo_maquina='1').count()
    numMoto103 = Maquina.objects.filter(tipo_maquina='2').count()
    # mostramos las máquinas pertenecientes a la obra 0748241
    # también mostramos cada tipo de máquina de esta obra
    numMaquinaObra0748241 = Maquina.objects.filter(obra__nombre_obra__exact='1').count()
    numDesbro_0748241 = Maquina.objects.filter(obra__nombre_obra__exact='1').filter(tipo_maquina='3').count()
    numMoto241_0748241 = Maquina.objects.filter(obra__nombre_obra__exact='1').filter(tipo_maquina='4').count()
    numMoto261_0748241 = Maquina.objects.filter(obra__nombre_obra__exact='1').filter(tipo_maquina='5').count()
    numMoto101_0748241 = Maquina.objects.filter(obra__nombre_obra__exact='1').filter(tipo_maquina='1').count()
    numMoto103_0748241 = Maquina.objects.filter(obra__nombre_obra__exact='1').filter(tipo_maquina='2').count()

    cerrado = Maquina.objects.filter(incidencias__cerrado=False)

    # movimientos = Maquina.maquina_poblacion.poblacion_mm.order_by('-fecha_movimiento')[0]
    llegandoCerrado = Maquina.objects.select_related(
        'tipo_maquina', 'capataz_responsable',
    ).prefetch_related('incidencias')
    return render(request,
                  'UPR/inventario_maquinas.html',
                  {'maquinas': maquinas,
                   'desbro': desbro,
                   'moto261': moto261,
                   'moto241': moto241,
                   'moto101': moto101,
                   'moto103': moto103,
                   'llegandoCerrado': llegandoCerrado,
                   'numMaquina': numMaquina,
                   'numMaquinaObra0748241': numMaquinaObra0748241,
                   'numDesbro': numDesbro,
                   'numMoto261': numMoto261,
                   'numMoto241': numMoto241,
                   'numMoto101': numMoto101,
                   'numMoto103': numMoto103,
                   'numDesbro_0748241': numDesbro_0748241,
                   'numMoto241_0748241': numMoto241_0748241,
                   'numMoto261_0748241': numMoto261_0748241,
                   'numMoto101_0748241': numMoto101_0748241,
                   'numMoto103_0748241': numMoto103_0748241,
                   'cerrado': cerrado,
                   'poblacion': poblacion,
                   })


# --------------- Maquina Details --------------- #
# /upr/maquina/721721/

def maquina_detail(request, ninventario):
    maquina = get_object_or_404(Maquina.objects.select_related(
                                            'tipo_maquina','capataz_responsable',
    ).prefetch_related('incidencias').order_by('indicencias__fecha'),
                                numero_inventario=ninventario)

    componentes = Componentes.objects.all().filter(tipo_maquina=maquina.tipo_maquina)
    movimientos = maquina.maquina_poblacion.all().order_by('-fecha_movimiento')[:1]
    incidencias = maquina.incidencias.all()
    grupos_componentes = GrupoComponentes.objects.all()
    mantenimiento_maquinaria = MantenimientoMaquinaria.objects.all().filter(numero_maquina=maquina.id)
    movimientosObra = maquina.obra.all().order_by('-fecha_movimiento')[:1]

    return render(request,
                  'UPR/detail.html',
                  {'maquina': maquina,
                   'ninventario': ninventario,
                   'componentes': componentes,
                   'movimientos': movimientos,
                   'incidencias': incidencias,
                   'grupos_componentes': grupos_componentes,
                   'mantenimiento_maquinaria': mantenimiento_maquinaria,
                   'movimientosObra' : movimientosObra
                   })

# --------------- Componente Details --------------- #
# /upr/componente/23/

def componente_detail(request, ncomponente, ecerrado, etaller):

    incidencias = Incidencias.objects.all().filter(cerrado=ecerrado).filter(taller=etaller).filter(tipo_incidencias=ncomponente).order_by('fecha')[:100]
    nIncidencias = incidencias.count()
    grupos_componentes = GrupoComponentes.objects.all().order_by('position_grupo_componentes')
    form = MaquinaIncidenciasForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            messages.success(request, "Incidencia creada.")
            return HttpResponseRedirect(reverse('upr:componente_detail', kwargs={'ncomponente': form['tipo_incidencias'].value(), 'ecerrado': form['cerrado'].value(), 'etaller': form['taller'].value()}))
        else:
            messages.error(request, "Error creando la incidencia.")

    return render(request,
                  'UPR/componente.html',
                  {'incidencias': incidencias,
                   'grupos_componentes': grupos_componentes,
                   'form': form,
                   'nIncidencias': nIncidencias,
                   })

# --------------- ultimas incidencias --------------- #
# /upr/ultimasincidencias/
def ultimas_incidencias(request):
    incidencias = Incidencias.objects.all().order_by('-updated')
    paginator = Paginator(incidencias, 100)

    page = request.GET.get('page')
    try:
        incidencias = paginator.page(page)
    except PageNotAnInteger:
        incidencias = paginator.page(1)
    except EmptyPage:
        indicencias = paginator.page(paginator.num_pages)
    return render(request,
                  'UPR/ultimasincidencias.html',
                  {'incidencias': incidencias
                   })

# --------------- protector_cuchilla --------------- #
# /upr/protectorcuchilla/
def protector_cuchilla(request):
    incidencias = Incidencias.objects.all().filter(cerrado=False).filter(tipo_incidencias=6).order_by('-created')[:100]

    return render(request,
                  'UPR/protectorcuchilla.html',
                  {'incidencias': incidencias,})



# --------------- Add_Incidencia --------------- #
def add_incidencia(request, ninventario):
    form = MaquinaIncidenciasForm(request.POST or None, request.FILES or None)
    maquina = get_object_or_404(Maquina.objects.select_related(
                                            'tipo_maquina','capataz_responsable',
                                        ).prefetch_related('incidencias').order_by('indicencias__fecha'),
                                numero_inventario=ninventario)

    grupos_componentes = GrupoComponentes.objects.all().order_by('position_grupo_componentes')
    componentes = Componentes.objects.all().filter(grupo_componentes__id=1)
    todosComponentes = Componentes.objects.select_related('grupo_componentes').prefetch_related('tipo_maquina','opciones_componente')
    print(componentes)

    if request.method == "POST":
        if form.is_valid():
            # Create, but don't save the new incidencia instance.
            instance = form.save(commit=False)
            # Save the new instance.
            instance.save()
            maquina.incidencias.add(instance)
            maquina.save()
            # Flash message
            messages.success(request, "Incidencia creada.")
            # Redirect
            return HttpResponseRedirect(reverse('upr:maquina_detail', kwargs={'ninventario':ninventario}))
        else:
            messages.error(request, "Error creando la incidencia.")

    return render(request,
              'UPR/incidencias.html',
              {'maquina': maquina,
               'ninventario': ninventario,
               'grupos_componentes': grupos_componentes,
               'form': form,
               'todosComponentes': todosComponentes
               })

# --------------- Ajax: Get all componentes from a specific Group --------------- #
def get_components_by_group(request):
    grupo_comp_id = request.GET.get('grupo_comp_id', '0')
    componentes = Componentes.objects.all().filter(grupo_componentes__id=grupo_comp_id)
    data = serializers.serialize('json', componentes)
    return HttpResponse(data, content_type="application/json")

# --------------- Ajax: Get all componentes from a specific Component --------------- #
def get_components_by_tipo_comentario(request):
    tipo_comentario_id = request.GET.get('tipo_comentario_id', '0')
    comentario = Componentes.objects.all().filter(id=tipo_comentario_id)
    data = serializers.serialize('json', comentario)
    return HttpResponse(data, content_type="application/json")

# --------------- Add_Ubicacion --------------- #
def add_ubicacion(request, ninventario):
    form = MovimientoMaquinariaForm(request.POST or None, request.FILES or None)
    maquina = get_object_or_404(Maquina.objects.select_related(
                                            'tipo_maquina','capataz_responsable',
                                        ).prefetch_related('maquina_poblacion').order_by('maquina_poblacion__fecha_movimiento'),
                                numero_inventario=ninventario)

    movimientos = maquina.maquina_poblacion.all().order_by('-fecha_movimiento')
    poblacion = Poblacion.objects.all()
    
    if request.method == "POST":
        if form.is_valid():
            # Create, but don't save the new ubicacion instance.
            instance = form.save(commit=False)
            # Save the new instance.
            instance.save()
            maquina.maquina_poblacion.add(instance)
            maquina.save()
            # Flash message
            messages.success(request, "Ubicación añadida.")
            # Redirect
            return HttpResponseRedirect(reverse('upr:maquina_detail', kwargs={'ninventario':ninventario}))
        else:
            messages.error(request, "Error añadiendo la ubicación.")

    return render(request,
              'UPR/ubicacion.html',
              {'maquina': maquina,
               'ninventario': ninventario,
               'poblacion': poblacion,
               'movimientos': movimientos,
               'form': form
               })


# --------------- Add_Obra --------------- #
def add_obra(request, ninventario):
    form = MovimientoObraForm(request.POST or None, request.FILES or None)
    maquina = get_object_or_404(Maquina.objects.select_related(
                                            'tipo_maquina','capataz_responsable',
                                        ).prefetch_related('obra').order_by('obra__fecha_movimiento'),
                                numero_inventario=ninventario)

    movimientos = maquina.obra.all().order_by('-fecha_movimiento')
    obra = Obra.objects.all()
    print(obra)

    if request.method == "POST":
        if form.is_valid():
            # Create, but don't save the new ubicacion instance.
            instance = form.save(commit=False)
            # Save the new instance.
            instance.save()
            maquina.obra.add(instance)
            maquina.save()
            # Flash message
            messages.success(request, "Obra cambiada.")
            # Redirect
            return HttpResponseRedirect(reverse('upr:maquina_detail', kwargs={'ninventario':ninventario}))
        else:
            messages.error(request, "Error cambiando la obra.")

    return render(request,
              'UPR/obra.html',
              {'maquina': maquina,
               'ninventario': ninventario,
               'obra': obra,
               'movimientos': movimientos,
               'form': form
               })
