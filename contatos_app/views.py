from django.shortcuts import render
from rest_framework import viewsets
from .models import Contato
from .serializers import ContatoSerializers

#Viewset - responsável por lidar com requisições (GET, POST, PUT, DELETE)
class ContatoViewSet(viewsets.ModelViewSet):
    queryset = Contato.objects.all() #Query que define que todos os objetos serão manipulados
    serializer_class = ContatoSerializers #transforma os dados em JSON