from home import forms
from home.forms import RegistroForm
from home.models import TagBle, Pessoa
from django.contrib import messages, auth
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

def index(request):
    # Define o contexto com as tags recuperadas
    context = {
        'site_title': 'Home | ',
    }

    # Renderiza o template 'home/index.html' com o contexto e retorna a resposta
    return render(request, 'home/index.html', context)

def tags(request):
    filtro = request.GET.get('filtro')  # Obtém o valor do parâmetro 'filtro' da URL
    if filtro == 'vinculadas':
        tags = TagBle.objects.exclude(monitorado=None)  # Filtra apenas as tags com monitorado vinculado
    else:
        tags = TagBle.objects.all()  # Obtém todas as tags

    paginator = Paginator(tags, 10)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'tags': tags,
        'page_obj': page_obj,
        'site_title': 'Tags | ',
    }
    return render(request, 'home/tags.html', context)

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

def criar_tag(request):
    if request.method == 'POST':
        form = forms.TagBleForm(request.POST)
        context = {
        'form': form
        }
        
        if form.is_valid():
            form.save()
            return redirect('tags')
        
        return render(request, 'home/criar_tag.html', context)
    
    context = {
        'form': forms.TagBleForm()
    }
    return render(request, 'home/criar_tag.html', context)

def criar_paciente(request):
    
    if request.method == 'POST':
        form = forms.PacienteForm(request.POST)
        context = {
            'form': form
        }

        if form.is_valid():
            form.save()

        return render(request, 'home/criar_paciente.html', context)

    context = {
        'form': forms.PacienteForm()
    }
    return render(request, 'home/criar_paciente.html', context)

def registrar_usuario(request):
    form = RegistroForm()


    if request.method == 'POST':
        form = RegistroForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário registrado')
            return redirect('login')

    return render(
        request,
        'home/registrar_usuario.html',
        {
            'form': form,
        }
        )

def login_view(request):
    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, f'Olá, {user.first_name}' )
            return redirect('index')
        else:
            messages.error(request, 'Usuário ou senha inválidos')

    return render(
        request,
        'home/login.html',
        {
            'form': form,
        }
        )

def logout_view(request):
    auth.logout(request)
    return redirect('login')
"""
Neste código:

A função index é uma função de visualização Django que manipula a solicitação HTTP para a página inicial do site.
Dentro da função, as tags com status 'novo' são recuperadas do banco de dados e ordenadas por ID em ordem decrescente.
Um contexto é criado com as tags recuperadas para ser passado para o template.
O template 'home/index.html' é renderizado com o contexto fornecido e a resposta HTTP resultante é retornada.
"""