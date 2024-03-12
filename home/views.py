from django.shortcuts import render
from home.models import TagBle, Pessoa
from django.core.paginator import Paginator

def index(request):
    # Define o contexto com as tags recuperadas
    context = {
        'site_title': 'Home | ',
    }

    # Renderiza o template 'home/index.html' com o contexto e retorna a resposta
    return render(request, 'home/index.html', context)

def get_tags(request):
    tags_ble = TagBle.objects.filter(status='novo').order_by('-id')
    
    paginator = Paginator(tags_ble, 10)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Define o contexto com as tags recuperadas
    context = {
        'page_obj': page_obj,
        'site_title': 'Tags | ',
    }

    # Renderiza o template 'home/index.html' com o contexto e retorna a resposta
    return render(request, 'home/tags.html', context)

def get_pessoas(request):
    pessoas = Pessoa.objects.all()
    #print(pessoas.query)

    context = {
        'pessoas': pessoas,
        'site_title': 'Pessoas | ',
    }
    return render(request,'home/pessoas.html', context)

"""
Neste código:

A função index é uma função de visualização Django que manipula a solicitação HTTP para a página inicial do site.
Dentro da função, as tags com status 'novo' são recuperadas do banco de dados e ordenadas por ID em ordem decrescente.
Um contexto é criado com as tags recuperadas para ser passado para o template.
O template 'home/index.html' é renderizado com o contexto fornecido e a resposta HTTP resultante é retornada.
"""