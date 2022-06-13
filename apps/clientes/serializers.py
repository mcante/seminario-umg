from rest_framework import serializers
from django.contrib.auth.models import User
from .models import NegocioCliente, Cliente




# Rest NegocioCliente
class NegocioClienteModelSerializer(serializers.ModelSerializer):
    cliente = serializers.StringRelatedField()
    negocio = serializers.StringRelatedField()
    
    class Meta:
        model = NegocioCliente
        fields = (  'id', 
                    'cliente', 
                    'negocio')


# Rest Cliente
class ClienteModelSerializer(serializers.ModelSerializer):
    empleado_asignado = serializers.StringRelatedField(source = 'empleado_asignado.get_full_name', default=None) # Busca el nombre completo y el resultado es nulo entonces se pasa default con None
    
    class Meta:
        model = Cliente
        fields = (  'id', 
                    'nombre_empresa', 
                    'nombre_contacto',
                    'email',
                    'telefono',
                    'nit',
                    'empleado_asignado'
                    )


# Rest Cliente Público
class ClientePublicModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cliente
        fields = (  'id', 
                    'nombre_empresa', 
                    'nombre_contacto',
                    'email',
                    'telefono',
                    'nit',
                    'empleado_asignado',
                    'key_access'
                    )
        

# Rest NegocioCliente Público
class NegocioClientePublicModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NegocioCliente
        fields = (  'id', 
                    'cliente', 
                    'negocio')
        depth = 1                    