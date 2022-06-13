from rest_framework import serializers
from django.contrib.auth.models import User

from .models import LogVelocidadesGPS, LogTiemposGPS



# Rest LogVelocidadesGPS
class LogVelocidadesGPSModelSerializer(serializers.ModelSerializer):
    #dispositivo_gps = serializers.StringRelatedField(source = 'dispositivo_gps.identificador', default=None)
    
    class Meta:
        model = LogVelocidadesGPS
        fields = (  'id', 
                    'dispositivo_gps', 
                    'velocidad_km',
                    'latitud',
                    'longitud'
                    )


# Rest LogTiemposGPS
class LogTiemposGPSModelSerializer(serializers.ModelSerializer):
    #dispositivo_gps = serializers.StringRelatedField(source = 'dispositivo_gps.identificador', default=None)
    
    class Meta:
        model = LogTiemposGPS
        fields = (  'id', 
                    'dispositivo_gps', 
                    'registro_inicio',
                    'latitud_inicio',
                    'longitud_inicio',
                    'registro_fin',
                    'latitud_fin',
                    'longitud_fin'
                    )
