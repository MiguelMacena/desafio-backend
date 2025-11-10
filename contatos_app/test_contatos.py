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

@pytest.mark.django_db
def test_criar_contato_invalido(api_client):
    url = reverse("contato-list")
    data = {"nome": "Sem Email"}
    response = api_client.post(url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_listar_contato(api_client, contato_exemplo): #indica que o teste vai acessar o banco de dados - teste cria e consulta objetos Contato
    url = reverse ("contato-list") #rota da lista de contatos GET e POST
    response = api_client.get(url) 
    assert response.status_code == 200 #valida se deu certo a requisição

    data = response.json()
    assert any
    (c["nome"] == "Miguel Teste" and c ["email"] == "miguel@teste.com"
      for c in data), 
    f"Contato esperado não encontrado em:{data}" #lista os dados em .json e acusa o erro

@pytest.mark.django_db
def test_editar_contato(api_client, contato_exemplo):
    url = reverse("contato-detail", args=[contato_exemplo.id]) # reverse gera uma URL automática a partir do nome da rota/ parametro args insere o ID do contato na URL
    data = {"nome": "Miguel Atualizado"}
    response = api_client.patch(url, data, format='json') 
    assert response.status_code == 200 #valida se deu tudo certo na requisição
    contato_exemplo.refresh_from_db() #atualiza com os dados mais recentes o Banco de Dados
    assert contato_exemplo.nome == "Miguel Atualizado" #valida se o nome foi alterado corretamente no Banco de Dados após a requisição

@pytest.mark.django_db
def test_excluir_contato(api_client, contato_exemplo):#objetos necessários
    url = reverse ("contato-detail", args=[contato_exemplo.id]) #reverse gera URL de acordo com o nome da rota / args traz o id automático do contato
    response = api_client.delete(url) #o retorno deve ser o DELETE do id buscado pelo args
    assert response.status_code == 204 #valida se deu tudo certo
    assert not Contato.objects.filter(id= contato_exemplo.id).exists() #faz uma consulta tentado encontrar o contato que foi deletado, o EXISTS retorna verdadeiro se existir e o NOT inverte isso