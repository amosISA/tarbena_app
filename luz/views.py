from django.core import serializers
from django.contrib.auth.decorators import login_required, permission_required
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
class ChartData(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
        query = Factura.objects.all().select_related(
            'contador',
        )
        data = serializers.serialize('json', query)
        return Response(data)