from rest_framework import generics
from ..models import Holiday
from .serializers import HolidaySerializer

class HolidayListView(generics.ListAPIView):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer

class HolidayDetailView(generics.RetrieveAPIView):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer