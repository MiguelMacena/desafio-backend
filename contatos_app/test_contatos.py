import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from contatos_app.models import Contato

@pytest.fixture 

def api_client(): #simula requisições HTTP como se fosse um usuário real
    return APIClient()

@pytest.fixture
def contato_exemplo(db): #cria um registro real no Bd de testes
    return Contato.objects.create(

        nome="Miguel Teste",
        email= "miguel@teste.com",
        telefone= "8499999999"
    )

@pytest.mark.django_db #indica que o teste vai acessar o banco de dados - teste cria e consulta objetos Contato
def test_criar_contato(api_client):
    url = reverse ("contato-list") #rota da lista de contatos GET e POST
    data = {
        "nome": "Novo Contato",
        "email": "miguel@test.com",
        "telefone": "8499999999"
    }
    response = api_client.post(url, data, format='json') #envia a requisição POST simulando criação de um novo contato 
    assert response.status_code == 201 #Valida se foi criado
    assert Contato.objects.filter(nome = "Novo Contato").exists() #faz a confirmação se o contato foi realmente criado
