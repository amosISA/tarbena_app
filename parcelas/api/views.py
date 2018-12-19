from rest_framework import generics
from ..models import Parcela
from .serializers import ParcelasSerializer

class ParcelasListView(generics.ListAPIView):
    queryset = Parcela.objects.all().prefetch_related(
        'sector_trabajo'
    ).select_related(
        'propietario', 'poblacion', 'estado', 'estado_parcela_trabajo'
    ).filter(sector_trabajo=1)
    serializer_class = ParcelasSerializer

class ParcelasBySectorView(generics.RetrieveAPIView):
    queryset = Parcela.objects.all().prefetch_related(
        'sector_trabajo'
    ).select_related(
        'propietario', 'poblacion', 'estado', 'estado_parcela_trabajo'
    )
    serializer_class = ParcelasSerializer

class GetParcelasBySector(generics.ListAPIView):
    serializer_class = ParcelasSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        sector = self.kwargs['sector']
        return Parcela.objects.all().prefetch_related(
            'sector_trabajo'
        ).select_related(
            'propietario', 'poblacion', 'estado', 'estado_parcela_trabajo'
        ).filter(sector_trabajo=sector)