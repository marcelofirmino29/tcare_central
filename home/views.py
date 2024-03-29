from home import forms
from home.forms import RegistroForm
from home.models import TagBle, Monitorado, Pessoa, Local, Paciente, Medico, Acompanhante, Enfermeiro, Raspberry, LeituraTag
from django.contrib import messages, auth
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
import plotly.graph_objs as go
import colorsys, random
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def index(request):
    # Define o contexto com as tags recuperadas
    context = {
        'site_title': 'Home | ',
    }

    # Renderiza o template 'home/index.html' com o contexto e retorna a resposta
    return render(request, 'home/index.html', context)

@login_required(login_url='login')
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

@login_required(login_url='login')
def pessoas(request):
    filtro = request.GET.get('filtro')  # Obtém o valor do parâmetro 'filtro' da URL
    if filtro == 'vinculadas':
        pessoas = Pessoa.objects.exclude(tag_ble=None)  # Filtra apenas as tags com monitorado vinculado
    else:
        pessoas = Pessoa.objects.all()  # Obtém todas as tags

    paginator = Paginator(pessoas, 10)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'pessoas': pessoas,
        'page_obj': page_obj,
        'site_title': 'Pessoas | ',
    }
    return render(request,'home/pessoas.html', context)

@login_required(login_url='login')
def cadastrar_tag(request):
    if request.method == 'POST':
        form = forms.TagBleForm(request.POST)
        context = {
        'form': form
        }
        
        if form.is_valid():
            form.save()
            return redirect('tags')
        
        return render(request, 'home/cadastrar_tag.html', context)
    
    context = {
        'form': forms.TagBleForm()
    }
    return render(request, 'home/cadastrar_tag.html', context)

@login_required(login_url='login')
def cadastrar_paciente(request):
    
    if request.method == 'POST':
        form = forms.PacienteForm(request.POST)
        context = {
            'form': form
        }

        if form.is_valid():
            form.save()

        return render(request, 'home/cadastrar_paciente.html', context)

    context = {
        'form': forms.PacienteForm()
    }
    return render(request, 'home/cadastrar_paciente.html', context)

@login_required(login_url='login')
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

@login_required(login_url='login')
def logout_view(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    total_pessoas = Pessoa.objects.exclude(tag_ble=None).count()
    locais = Local.objects.all()
    ultimas_leituras = LeituraTag.objects.order_by('-id').filter()[:50] #no contexto estou passando apenas 12 leituras
    ultimos_pacientes = []
    ultimos_acompanhantes = []
    ultimos_medicos = []
    for leitura in ultimas_leituras:
        if Paciente.objects.filter(monitorado_ptr=leitura.monitorado):
            ultimos_pacientes.append(leitura)
        elif Acompanhante.objects.filter(monitorado_ptr=leitura.monitorado):
            ultimos_acompanhantes.append(leitura)
        elif Medico.objects.filter(monitorado_ptr=leitura.monitorado):
            ultimos_medicos.append(leitura)





    pessoas_por_local = {}

    locais_com_pessoas = [local for local in locais if Pessoa.objects.filter(local_atual=local).exists()]


    for local in locais_com_pessoas:
        pessoas_por_local[local.localizacao] = Pessoa.objects.filter(local_atual=local).count()
    
    # Em seguida, extraímos os IDs dos pacientes associados a essas leituras
    

    pacientes = Paciente.objects.exclude(tag_ble=None)
    total_pacientes = pacientes.count()
    medicos = Medico.objects.exclude(tag_ble=None)
    total_medicos = medicos.count()
    acompanhantes = Acompanhante.objects.exclude(tag_ble=None)
    total_acompanhantes = acompanhantes.count()
    enfermeiros = Enfermeiro.objects.exclude(tag_ble=None)
    total_enfermeiros = enfermeiros.count()

     # Criar dados para o gráfico de pizza
    labels = list(pessoas_por_local.keys())
    values = list(pessoas_por_local.values())

    # Criar texto personalizado para cada fatia
    #text_info = [f"{label}: {value} " for label, value in zip(labels, values)]
    text_info = [f"<a target='_self' href='/local/{label}'>{label}: {value}</a> " for label, value in zip(labels, values)]

    # Definir cor principal (RGB)
    main_color = (0, 90, 80)

    # Converter cor principal para HSL
    hsl_color = colorsys.rgb_to_hls(main_color[0] / 255, main_color[1] / 255, main_color[2] / 255)

    # Definir cores para as fatias do gráfico de pizza com diferentes intensidades
    num_slices = len(labels)
    colors = [f'hsl({hsl_color[0] * 360}, 50%, {70 - i*(50/num_slices)}%)' for i in range(num_slices)]
    

    # Criar gráfico de pizza
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, text=text_info, hole=0.3, marker=dict(colors=colors, 
                line=dict(color='#000000', width=2)), hoverinfo='label+percent+value', textinfo='text+percent', 
                insidetextorientation='radial', pull=[0.1, 0.1, 0.1, 0.1])])

    # Definir layout
    fig.update_layout(title='Distribuição de Pessoas por Área')

    # Converter a figura para HTML
    graph_html = fig.to_html(full_html=False)


    context = {
        'total_pessoas': total_pessoas,
        'pessoas_por_local': pessoas_por_local,
        'pacientes': pacientes,
        'total_pacientes': total_pacientes,
        'medicos': medicos,
        'total_medicos': total_medicos,
        'acompanhantes': acompanhantes,
        'total_acompanhantes': total_acompanhantes,
        'enfermeiros': enfermeiros,
        'total_enfermeiros': total_enfermeiros,
        'graph_html': graph_html,
        'ultimas_leituras': ultimas_leituras[:12],
        'ultimos_pacientes': ultimos_pacientes,
        'ultimos_acompanhantes': ultimos_acompanhantes,
        'ultimos_medicos': ultimos_medicos,

    }
    

    return render(request,'home/dashboard.html', context)
@login_required(login_url='login')
def local_detalhes(request, local_localizacao):
    local = get_object_or_404(Local,localizacao=local_localizacao)
    pessoas_no_local = Pessoa.objects.filter(local_atual=local)

    context = {
        'local': local,
        'pessoas_no_local': pessoas_no_local
    }

    return render(request, 'home/local_detalhes.html', context)

@login_required(login_url='login')
def simula_leitura(request):
    raspberry = random.choice(Raspberry.objects.all())
    tag_ble = random.choice(TagBle.objects.exclude(monitorado=None))
    local = Local.objects.get(raspberry=raspberry)
    monitorado = Monitorado.objects.get(tag_ble=tag_ble)
    leitura = LeituraTag.objects.create(
        tag_ble=tag_ble,
        raspberry=raspberry,
        monitorado=monitorado,
        data_leitura=timezone.now(),
        local=local
    )

    if monitorado.local_atual != local:
        monitorado.local_atual = local
        monitorado.save()

    context = {
        'leitura': leitura,
    }

    return render(request, 'home/leitura_tag.html', context)

@login_required(login_url='login')
def leituras(request):
    leituras = LeituraTag.objects.all().order_by('id')
    monitorados = set(leitura.monitorado for leitura in leituras)
    locais = set(leitura.local for leitura in leituras)
    

    # Filtrando por monitorado
    monitorado_id = request.GET.get('monitorado')
    if monitorado_id:
        leituras = leituras.filter(monitorado_id=monitorado_id).order_by('id')

    # Filtrando por local
    local_id = request.GET.get('local')
    if local_id:
        leituras = leituras.filter(local_id=local_id).order_by('id')

    # Filtrando por data
    data = request.GET.get('data')

    if data:
        # Supondo que a data seja passada no formato YYYY-MM-DD
        leituras = leituras.filter(data_leitura__date=data).order_by('id')


    paginator = Paginator(leituras, 20)  # 20 leituras por página
    page_number = request.GET.get('page')
    leituras = paginator.get_page(page_number)

    context = {
        'leituras': leituras,
        'monitorados': monitorados,
        'locais': locais,
    }

    return render(request, 'home/leituras.html', context)

@login_required(login_url='login')
def vincular_tag_pessoa(request):

    if request.method == 'POST':
        tag_id = request.POST.get('tag_id')
        monitorado_id = request.POST.get('monitorado_id')

        if tag_id and monitorado_id:
            try:
                # Obtendo a tag e o monitorado correspondentes às IDs fornecidas
                tag = TagBle.objects.get(id=tag_id)
                monitorado = Monitorado.objects.get(id=monitorado_id)

                # Vinculando a tag ao monitorado
                monitorado.tag_ble = tag
                monitorado.save()

                messages.success(request, f'Tag {tag} vinculada a {monitorado}')

                return redirect('tags')
            except (TagBle.DoesNotExist, Monitorado.DoesNotExist):
                messages.error(request, 'Erro. Tag não vinculada')


    tags_ble = TagBle.objects.filter(monitorado=None)
    monitorados = Monitorado.objects.filter(tag_ble=None)

    context = {
        'tags_ble': tags_ble,
        'monitorados': monitorados
    }
    return render(request, 'home/vincular_tag_pessoa.html', context)