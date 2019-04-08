from django.core import serializers
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Factura, Contador
import rest_framework

# Create your views here.
# --------------- Luz Index --------------- #
@login_required()
@permission_required('subvenciones.add_subvencion', raise_exception=True)
def index_facturas(request):
    contadores = Contador.objects.all()
    return render(request,
                  'luz/index.html',
                  {'contadores':contadores})

# --------------- Facturas JSON --------------- #
@login_required()
@permission_required('subvenciones.add_subvencion', raise_exception=True)
def get_data(request, *args, **kwargs):
    query = Factura.objects.all().select_related(
        'contador',
    )
    data = serializers.serialize('json', query)
    return HttpResponse(data, content_type="application/json")

# --------------- Facturas JSON RestFramework - More features with Authentication and Authorization --------------- #
class AdminAuthenticationPermission(rest_framework.permissions.BasePermission):
    """
    Only users that are superusers can access the API
    """

    ADMIN_ONLY_AUTH_CLASSES = [rest_framework.authentication.BasicAuthentication, rest_framework.authentication.SessionAuthentication]

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated():
            return user.is_superuser or \
                not any(isinstance(request._authenticator, x) for x in self.ADMIN_ONLY_AUTH_CLASSES)
        return False

class ContadoresTotalConsumo(APIView):
    """
    All Contadores with their FULL Consumo returned from all years
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, AdminAuthenticationPermission,)

    def get(self, request, format=None):
        query = Factura.objects.select_related('contador', ).values('contador__nombre').order_by(
            'contador__nombre').annotate(consumo=Sum('consumo'))
        contador = list(map(lambda x : x['contador__nombre'], query))
        consumo = list(map(lambda x : x['consumo'], query))
        data = {
            'contador': contador,
            'consumo': consumo
        }
        return Response(data)

def totalConsumoByContador(request, contador_id):
    """
    Individual Contador Consumo returned from all years
    """
    contador_consumo = Factura.objects.all().select_related(
        'contador',
    ).filter(contador__id=contador_id).order_by('desde')

    data = serializers.serialize('json', contador_consumo)
    return HttpResponse(data, content_type="application/json")