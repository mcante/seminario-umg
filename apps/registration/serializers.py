from rest_framework import serializers
from .models import NegocioUsuario



# Rest Negocios asignados al Usuario
class NegocioUsuarioModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = NegocioUsuario
        fields = (  'id', 
                    'preferido'
                    )