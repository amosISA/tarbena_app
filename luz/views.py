from django.core import serializers
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Factura

# Create your views here.
# --------------- Luz Index --------------- #
def index_facturas(request):
    return render(request,
                  'luz/index.html',
                  {})

# --------------- Facturas JSON --------------- #
def get_data(request, *args, **kwargs):
    query = Factura.objects.all().select_related(
        'contador',
    )
    data = serializers.serialize('json', query)
    return HttpResponse(data, content_type="application/json")

# --------------- Facturas JSON RestFramework - More features with Authentication and Authorization --------------- #
class ContadorTotalConsumo(APIView):
    authentication_classes = ()
    permission_classes = ()

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