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

#teste de integração geral - pytest
@pytest.mark.django_db
def test_fluxo_completo_contato(api_client):
    create_url = reverse("contato-list") #nome registrado no router do View Set
    data = {"nome":"Miguel", "email":"miguel@teste.com", "telefone":"1199999999"} #dados simulados para POST
    response = api_client.post(create_url, data, format="json") #garante o formato Json e fornece o tipo de requisição desejada
    assert response.status_code == 201 # garante se retornou 201 Created
    contato_id = response.json()["id"] #pega o ID do contato criado

    list_response = api_client.get(create_url) #lista contatos e valida se o novo está criado
    assert any(c["id"] == contato_id for c in list_response.json()) #valida se o contato recem-criado está presente na lista

    update_url = reverse("contato-detail", args=[contato_id]) #pega o ID para inserir na rota do PATCH
    update_data = {"nome": "Miguel Atualizado"} #Passa dado que será atualizado
    update_response = api_client.patch(update_url, update_data, format="json") #garante que o retorno seja em Json e informa a requisição que dever ser feita
    assert update_response.status_code == 200 #valida se retorna 200 Sucess

    delete_response = api_client.delete(update_url) # faz uma requisição delete na mesma URL
    assert delete_response.status_code == 204 #valida se retornou 204 - Sem conteudo

    final_list = api_client.get(create_url) #valida se o ID foi removido do banco 
    assert not any(c["id"] == contato_id for c in final_list.json())