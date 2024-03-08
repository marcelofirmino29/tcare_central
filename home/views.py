from django.shortcuts import render
from home.models import TagBle

def index(request):
    """
    Função de visualização para renderizar a página inicial.

    Parameters:
        request (HttpRequest): O objeto HttpRequest para a solicitação HTTP.

    Returns:
        HttpResponse: Uma resposta HTTP renderizada com o conteúdo da página inicial.
    """
    # Recupera todas as tags com status 'novo' e as ordena por ID em ordem decrescente
    tags = TagBle.objects.filter(status='novo').order_by('-id')

    # Define o contexto com as tags recuperadas
    context = {
        'tags': tags,
    }

    # Renderiza o template 'home/index.html' com o contexto e retorna a resposta
    return render(request, 'home/index.html', context)


"""
Neste código:

A função index é uma função de visualização Django que manipula a solicitação HTTP para a página inicial do site.
Dentro da função, as tags com status 'novo' são recuperadas do banco de dados e ordenadas por ID em ordem decrescente.
Um contexto é criado com as tags recuperadas para ser passado para o template.
O template 'home/index.html' é renderizado com o contexto fornecido e a resposta HTTP resultante é retornada.
"""