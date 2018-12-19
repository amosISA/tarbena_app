from rest_framework import serializers
from ..models import Parcela, Estado, SectorTrabajo

class EstadoParcelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ('nombre')

class ParcelasSerializer(serializers.ModelSerializer):
    #https://www.django-rest-framework.org/api-guide/relations/
    #propietario_name = serializers.CharField(source='propietario.natural_key')
    #estado_nombre = serializers.CharField(source='estado.nombre')
    #estados = EstadoParcelaSerializer(many=True, read_only=True)

    class Meta:
        model = Parcela
        #fields = '__all__'
        fields = ('id', 'propietario', 'poblacion', 'metros_cuadrados',
                  'poligono', 'numero_parcela', 'estado_parcela_trabajo', 'estado',
                  'comentarios', 'sector_trabajo')
        depth = 3