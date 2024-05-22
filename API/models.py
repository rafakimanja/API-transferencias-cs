from django.db import models

class Jogador(models.Model):

    nome = models.CharField(max_length=30)
    origem = models.CharField(max_length=30)
    destino = models.CharField(max_length=30)
    movimentacao = models.CharField(max_length=30, default='')

    def __str__(self) -> str:
        return self.nome