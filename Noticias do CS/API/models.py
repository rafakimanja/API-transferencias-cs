from django.db import models

class Jogador(models.Model):

    nome = models.CharField(max_length=20)
    origem = models.CharField(max_length=20)
    destino = models.CharField(max_length=20)
    movimentacao = models.CharField(max_length=20, default='')

    def __str__(self) -> str:
        return self.nome