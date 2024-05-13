from rest_framework import viewsets
from django.http import HttpResponse
from API.models import Jogador
from API.serializer import JogadorSerializer
import cloudscraper
from bs4 import BeautifulSoup


def raspagem_dados(frases):

    for frase in frases:  
        
        if 'transfers' in frase:

            palavras = frase.split()

            indice_transfers = palavras.index('transfers')
            indice_from = palavras.index('from')
            indice_to = palavras.index('to')

            nome_jogador = ' '.join(palavras[:indice_transfers])
            origem = ' '.join(palavras[indice_from+1:indice_to] )
            destino = ' '.join(palavras[indice_to+1:])

            if not Jogador.objects.filter(nome=nome_jogador, origem=origem, destino=destino, movimentacao='tranferência').exists():
                new_post = Jogador(nome=nome_jogador, origem=origem, destino=destino, movimentacao='tranferência')
                new_post.save()


        elif 'benched' in frase:
        
            palavras = frase.split()

            indice_is = palavras.index('is')
            indice_on = palavras.index('on')

            nome_jogador = ' '.join(palavras[:indice_is])
            time = ' '.join(palavras[indice_on+1:])

            if not Jogador.objects.filter(nome=nome_jogador, origem=time, destino='banco '+time, movimentacao='banco de reservas').exists():
                new_post = Jogador(nome=nome_jogador, origem=time, destino='banco '+time, movimentacao='banco de reservas')
                new_post.save()
            
        

        elif 'parts' in frase:

            palavras = frase.split()

            indice_parts = palavras.index('parts')
            indice_with = palavras.index('with')

            nome_jogador = ' '.join(palavras[:indice_parts])
            time = ' '.join(palavras[indice_with+1:])

            if not Jogador.objects.filter(nome=nome_jogador, origem=time, destino='sem time', movimentacao='saída').exists():
                new_post = Jogador(nome=nome_jogador, origem=time, destino='sem time', movimentacao='saída')
                new_post.save()


        elif 'joins' in frase:
            
            palavras = frase.split()

            indice_joins = palavras.index('joins')

            nome_jogador = ' '.join(palavras[:indice_joins])
            time = ' '.join(palavras[indice_joins+1:])

            if not Jogador.objects.filter(nome=nome_jogador, origem='sem time', destino=time, movimentacao='entrada').exists():
                new_post = Jogador(nome=nome_jogador, origem='sem time', destino=time, movimentacao='entrada')
                new_post.save()
                    


def main(request):
    
    if request.method == 'GET':

        link = 'https://www.hltv.org/transfers'

        scraper = cloudscraper.create_scraper()

        requisicao = scraper.get(link)

        if requisicao.status_code == 200:
            
            dados = []

            site = BeautifulSoup(requisicao.text, "html.parser")

            transferencias = site.find_all("div", class_='transfer-movement')


            for transferencia in transferencias:
                
                dados.append(transferencia.text)
            
            raspagem_dados(dados)

            return HttpResponse("Funcionou!")



class JogadoresViewSet(viewsets.ModelViewSet):
    queryset = Jogador.objects.all()
    serializer_class = JogadorSerializer
