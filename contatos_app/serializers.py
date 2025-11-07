from rest_framework import serializers
from .models import Contato

#Serializer - tem como função pegar a nossa classe de contatos e transformar em um json para uso de uma API
class ContatoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contato
        fields = '__all__' #força todos os campos serem incluidos