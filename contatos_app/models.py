from django.db import models

#criaçao da classe Contato com todos os dados necessários
class Contato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    data_criacao = models.DateTimeField(auto_now=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
