from rest_framework import serializers
from API.models import Jogador

class JogadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jogador
        fields = ['id', 'nome', 'origem', 'destino', 'movimentacao']
