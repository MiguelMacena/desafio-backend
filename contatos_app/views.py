from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.cache import cache
from django.conf import settings
from django.shortcuts import render
from rest_framework import viewsets
from .models import Contato
from .serializers import ContatoSerializers


CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 *5) #pega o valor atribuido no setting.py - Time To Live  e caso não exista o tempo padrão será de 5 minutos

#Viewset - responsável por lidar com requisições (GET, POST, PUT, DELETE)
class ContatoViewSet(viewsets.ModelViewSet):
    queryset = Contato.objects.all() #Query que define que todos os objetos serão manipulados
    serializer_class = ContatoSerializers #transforma os dados em JSON

    def list(self, request, *args, **kwargs): #controla o que acontece quando um cliente faz um GET em /api/contatos
        cache_key = "contatos_list" #define uma chave unica no cache que será usado para recuperar os dados do cache
        contatos = cache.get(cache_key) #tenta buscar os contatos que já estão no cache

        if not contatos: #se o cache estiver vazio
            queryset = self.get_queryset() # busca contatos no banco
            serializer = self.get_serializer(queryset, many =True) #converte a query em JSOn
            contatos = serializer.data
            cache.set(cache_key, contatos, timeout=CACHE_TTL) #salva os dados no cache e salva de acordo com o Time to Live
            origem = "DB" #informa que veio do banco
        else:
            origem = "CACHE" #informa que estava armazenado no cache
        return Response({"origem": origem, "data":contatos}) #retorna o HTTP em Json indicando a lista de contatos e também a origem
    
    def create(self, request, *args, **kwargs): #define o que acontecen quando há um POST para novo contato
        response = super().create(request, *args, **kwargs) #chama método original - valida dados, cria registro no bd- retorna a resposta HTTP 201, tudo isso é armazenado em RESPONSE
        cache.delete("contatos_list") #após a criação de um novo contato o código limpa o cache - evita um novo GET desatualizado
        return response
    
    def update(self, request, *args, **kwargs): #define quando há um novo PATCH
        response = super().update(request, *args, **kwargs) #método original e faz validações necesárias
        cache.delete("contatos_list") #após a edição ser realizada com sucesso é feito o delete do cache que estava presente
        return response
    
    def destroy(self, request, *args, **kwargs): #define quando há um novo DELETE
        response = super().destroy(request, *args, **kwargs) #método original e faz validações necessárias
        cache.delete("contatos_list") #após o DELETE ser realizado é feito o delete do cache que presente
        return response