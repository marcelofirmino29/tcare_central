from home import forms
from home.models import TagBle, Monitorado, Pessoa, Local, Paciente, Funcionario, Acompanhante, Raspberry, LeituraTag
from django.contrib import messages, auth
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
import plotly.graph_objs as go
import colorsys, random
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from collections import Counter
from django.utils.text import slugify
from django.db.models import Q

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
    elif filtro == 'disponiveis':
        tags = TagBle.objects.filter(monitorado=None)  # Filtra tags sem monitorado
    else:
         tags = TagBle.objects.all()  # Obtém todas as tags

    paginator = Paginator(tags, 20)  
    page_number = request.GET.get("page")
    tags_paginated = paginator.get_page(page_number)

    context = {
        'tags': tags_paginated,
        'site_title': 'Tags | ',
        'filtro': filtro,
        'form': forms.TagBleForm(),
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
            messages.success(request,"Tag cadastrada com sucesso")
            return redirect('cadastrar_tag')
        else:
            messages.error(request, 'Tag não cadastrada')
        
        return render(request, 'home/cadastrar_tag.html', context)
    
    context = {
        'form': forms.TagBleForm()
    }
    return render(request, 'home/cadastrar_tag.html', context)


@login_required(login_url='login')
def cadastrar_pessoa(request):
    
    if request.method == 'POST':
        form = forms.PessoaForm(request.POST)
        context = {
            'form': form
        }

        if form.is_valid():
            nome = form.cleaned_data['nome']
            tipo = form.cleaned_data['tipo']
            form.save()
            messages.success(request, f'{tipo} {nome} adicionado(a)')

        return render(request, 'home/cadastrar_pessoa.html', context)

    context = {
        'form': forms.PessoaForm()
    }
    return render(request, 'home/cadastrar_pessoa.html', context)



@login_required(login_url='login')
def cadastrar_paciente(request):
    
    if request.method == 'POST':
        form = forms.PacienteForm(request.POST)
        context = {
            'form': form
        }

        if form.is_valid():
            nome = form.cleaned_data['nome']
            form.save()
            messages.success(request, f'Paciente {nome} adicionado(a)')

        return render(request, 'home/cadastrar_paciente.html', context)

    context = {
        'form': forms.PacienteForm()
    }
    return render(request, 'home/cadastrar_paciente.html', context)


@login_required(login_url='login')
def cadastrar_acompanhante(request):
    
    if request.method == 'POST':
        form = forms.AcompanhanteForm(request.POST)
        context = {
            'form': form
        }

        if form.is_valid():
            nome = form.cleaned_data['nome']
            form.save()
            messages.success(request, f'Acompanhante {nome} adicionado(a)')

        return render(request, 'home/cadastrar_acompanhante.html', context)

    
    context = {
        'form': forms.AcompanhanteForm()
    }
    return render(request, 'home/cadastrar_acompanhante.html', context)


def cadastrar_funcionario(request):
    print('cadastrando funcionário')
    if request.method == 'POST':
        form = forms.FuncionarioForm(request.POST)
        context = {
            'form': form
        }

        if form.is_valid():
            nome = form.cleaned_data['nome']
            tipo = form.cleaned_data['tipo']
            form.save()
            messages.success(request, f'{tipo} {nome} adicionado(a)')
        
        return render(request, 'home/cadastrar_funcionario.html', context)
    
    context = {
        'form': forms.FuncionarioForm()
    }
    return render(request, 'home/cadastrar_funcionario.html',context)


@login_required(login_url='login')
def registrar_usuario(request):
    form = forms.RegistroForm()


    if request.method == 'POST':
        form = forms.RegistroForm(request.POST)

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
    form = forms.BootstrapAuthenticationForm(request)

    if request.method == 'POST':
        form = forms.BootstrapAuthenticationForm(request, data=request.POST)

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
    ultimas_leituras = LeituraTag.objects.order_by('-id').filter()[:11] 
    ultimos_pacientes = LeituraTag.objects.filter(monitorado__in=Pessoa.objects.filter(tipo=1)).order_by('-id')[:6]
    ultimos_acompanhantes = LeituraTag.objects.filter(monitorado__in=Pessoa.objects.filter(tipo=2)).order_by('-id')[:6]
    ultimos_medicos = LeituraTag.objects.filter(monitorado__in=Pessoa.objects.filter(tipo=3)).order_by('-id')[:6]
    ultimos_enfermeiros = LeituraTag.objects.filter(monitorado__in=Pessoa.objects.filter(tipo=4)).order_by('-id')[:6]

    pessoas_por_local = {}

    locais_com_pessoas = [local for local in locais if Pessoa.objects.exclude(tag_ble=None).filter(local_atual=local).exists()]


    for local in locais_com_pessoas:
        pessoas_por_local[local.localizacao] = Pessoa.objects.exclude(tag_ble=None).filter(local_atual=local).count()
    
    # Em seguida, extraímos os IDs dos pacientes associados a essas leituras
    

    pacientes = Pessoa.objects.exclude(tag_ble=None).filter(tipo=1)
    total_pacientes = pacientes.count()
    medicos = Pessoa.objects.exclude(tag_ble=None).filter(tipo=3)
    total_medicos = medicos.count()
    acompanhantes = Pessoa.objects.exclude(tag_ble=None).filter(tipo=2)
    total_acompanhantes = acompanhantes.count()
    enfermeiros = Pessoa.objects.exclude(tag_ble=None).filter(tipo=4)
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

    # Contar o número de pessoas por tipo (paciente, médico, acompanhante)
    total_por_tipo = Counter()
    total_por_tipo.update({'Paciente': total_pacientes, 'Médico': total_medicos, 'Enfermeiro': total_enfermeiros, 'Acompanhante': total_acompanhantes})

    # Criar dados para o gráfico de barras
    tipos = list(total_por_tipo.keys())
    quantidades = list(total_por_tipo.values())

    # Usar as mesmas cores do gráfico de pizza para o gráfico de barras
    bar_colors = colors[:len(tipos)]

    # Criar gráfico de barras
    bar_links = [f"<a href='/localizacao/?tipo={slugify(tipo)}' target='_self'>{tipo}</a>" for tipo in tipos] #TODO trocar o link, em vez de abrir leituras, abrir lista de pessoas por tipo

    fig_bar = go.Figure([go.Bar(
        x=bar_links,
        y=quantidades,
        marker_color=bar_colors,
        hoverinfo='x',
        text=quantidades,
        textposition='outside',
    )])


    # Definir layout
    fig_bar.update_layout(title='Total de Pessoas no Hospital por Tipo')

    # Converter a figura para HTML
    graph_bar_html = fig_bar.to_html(full_html=False)

    data_hoje = timezone.now().strftime("%Y-%m-%d")

    context = {
        'total_pessoas': total_pessoas,
        'pessoas_por_local': pessoas_por_local,
        'total_pacientes': total_pacientes,
        'total_medicos': total_medicos,
        'total_acompanhantes': total_acompanhantes,
        'total_enfermeiros': total_enfermeiros,
        'graph_html': graph_html,
        'graph_bar_html': graph_bar_html,
        'ultimas_leituras': ultimas_leituras,
        'ultimos_pacientes': ultimos_pacientes,
        'ultimos_acompanhantes': ultimos_acompanhantes,
        'ultimos_medicos': ultimos_medicos,
        'ultimos_enfermeiros': ultimos_enfermeiros,
        'data_hoje': data_hoje,

    }
    

    return render(request,'home/dashboard.html', context)


@login_required(login_url='login')
def localizacao(request):
    tipo = request.GET.get('tipo','todos')
    if tipo == 'medico':
        lista = Pessoa.objects.exclude(tag_ble=None).filter(tipo__tipo='Médico')
    elif tipo == 'acompanhante':
        lista = Pessoa.objects.exclude(tag_ble=None).filter(tipo__tipo='Acompanhante')
    elif tipo == 'enfermeiro':
        lista = Pessoa.objects.exclude(tag_ble=None).filter(tipo__tipo='Enfermeiro')
    elif tipo == 'paciente':
        lista = Pessoa.objects.exclude(tag_ble=None).filter(tipo__tipo='Paciente') 

    else:
        lista = Pessoa.objects.exclude(tag_ble=None)

    paginator = Paginator(lista, 20)  # 20 leituras por página
    page_number = request.GET.get('page')
    lista_paginated = paginator.get_page(page_number)
    
    context = {
        'tipo': tipo,
        'lista': lista_paginated
    }

    return render(request, 'home/localizacao.html', context)


@login_required(login_url='login')
def local_detalhes(request, local_localizacao):
    local = get_object_or_404(Local, localizacao=local_localizacao)
    pessoas_no_local = Pessoa.objects.exclude(tag_ble=None).filter(local_atual=local)
    count = pessoas_no_local.__len__
    leituras = LeituraTag.objects.filter(local=local)

    # Dicionário para armazenar o horário de entrada de cada pessoa
    lista_leituras = []

    # Iterar sobre as pessoas no local
    for pessoa in pessoas_no_local:
        # Filtrar leituras para a pessoa atual
        leituras_pessoa = leituras.filter(monitorado=pessoa.id)
        # Se houver leituras para a pessoa, encontrar a leitura mais antiga como horário de entrada
        if leituras_pessoa.exists():
            lista_leituras.append(leituras_pessoa.latest('data_leitura'))
    
    lista_leituras = sorted(lista_leituras, key=lambda leitura: leitura.id, reverse=True)



    context = {
        'lista_leituras': lista_leituras,  # Adicionando o horário de entrada ao contexto
        'local':local,
        'count': count
    }

    return render(request, 'home/local_detalhes.html', context)

@login_required(login_url='login')
def pessoa_detalhes(request):
    busca = request.GET.get('busca')
    pessoa = None
    
    if busca:
        busca = ''.join(filter(str.isdigit, busca))

    
    if busca:
        try:
            # Tenta buscar a pessoa por id (busca convertida para inteiro)
            pessoa = Pessoa.objects.filter(Q(id=int(busca)) | Q(cpf=busca)).first
        except (ValueError, Pessoa.DoesNotExist):
            # Se não encontrou por id ou por cpf, retorna None ou faça algo adequado ao seu caso
            pessoa = None



    context = {
        'pessoa': pessoa,
        'busca': busca,
    }

    return render(request,'home/pessoa_detalhes.html', context)

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
    leituras = LeituraTag.objects.all().order_by('-id')
    #monitorados = set(leitura.monitorado for leitura in leituras),
    #locais = set(leitura.local for leitura in leituras)
    # Obter parâmetros de filtro do GET
    monitorado_id = request.GET.get('monitorado')
    filtro_pessoa = request.GET.get('filtro-pessoa')
    filtro_tipo = request.GET.get('filtro-tipo')  
    local_id = request.GET.get('local')
    data = request.GET.get('data')
    tipo = request.GET.get('tipo')


    if filtro_tipo or filtro_pessoa:
        if filtro_tipo == 'cpf':
            pessoas_filtradas = Pessoa.objects.filter(cpf__icontains=filtro_pessoa)
            leituras = LeituraTag.objects.filter(monitorado__in=pessoas_filtradas)
        elif filtro_tipo == 'id':
            try:
                id_pessoa = int(filtro_pessoa)  # Converter filtro_pessoa para inteiro (se for um ID válido)
                pessoas_filtradas = Pessoa.objects.filter(id=id_pessoa)
                leituras = LeituraTag.objects.filter(monitorado__in=pessoas_filtradas)

            except ValueError:
                leituras = Pessoa.objects.none()  # Retorna uma queryset vazia se filtro_pessoa não for um número válido
        else:
            pessoas_filtradas = Pessoa.objects.filter(nome__icontains=filtro_pessoa)
            leituras = leituras.filter(monitorado__in=pessoas_filtradas)



    # Aplicar filtros conforme necessário
    if monitorado_id:
        leituras = leituras.filter(monitorado_id=monitorado_id)
    # if filtro_pessoa:
    #     pessoas_filtradas = Pessoa.objects.filter(nome__icontains=filtro_pessoa)
    #     leituras = leituras.filter(monitorado__in=pessoas_filtradas)
    if local_id:
        leituras = leituras.filter(local_id=local_id)
    if data:
        leituras = leituras.filter(data_leitura__date=data)
    if tipo:
        if tipo == 'paciente':
            leituras = leituras.filter(monitorado__in=Pessoa.objects.filter(tipo=1))
        elif tipo == 'acompanhante':
            leituras = leituras.filter(monitorado__in=Pessoa.objects.filter(tipo=2))
        elif tipo == 'medico':
            leituras = leituras.filter(monitorado__in=Pessoa.objects.filter(tipo=3))
        elif tipo == 'enfermeiro':
            leituras = leituras.filter(monitorado__in=Pessoa.objects.filter(tipo=4))



            


    paginator = Paginator(leituras, 20)  # 20 leituras por página
    page_number = request.GET.get('page')
    leituras_paginated = paginator.get_page(page_number)

    context = {
        'leituras': leituras_paginated,
        #'monitorados': monitorados,
        #'locais': locais,
        'filtro_pessoa': filtro_pessoa,
        'filtro_tipo': filtro_tipo,        
        'monitorado_id': monitorado_id,
        'local_id': local_id,
        'data': data,
        'tipo': tipo,

    }

    return render(request, 'home/leituras.html', context)


@login_required(login_url='login')
def vincular_tag_pessoa(request):
    resultados_da_busca = None
    resultados_da_busca_paginated = None
    if request.method == 'POST':
        tag_id = request.POST.get('tag_id')
        pessoa_id = request.POST.get('pessoa_id')

        if tag_id and pessoa_id:
            try:
                # Verifica se a tag existe e não está vinculada a uma pessoa
                tag = TagBle.objects.get(id=tag_id, monitorado=None)
                # Obtendo a pessoa correspondente à ID fornecida
                pessoa = Pessoa.objects.get(id=pessoa_id)

                # Vinculando a tag à pessoa
                pessoa.tag_ble = tag
                pessoa.local_atual = Local.objects.get(id=4) # local = aguardando leitura
                pessoa.save()

                LeituraTag.objects.create(
                    tag_ble=pessoa.tag_ble,
                    raspberry=Raspberry.objects.get(id=6), #rasp = aguardando leituras
                    monitorado=pessoa,
                    data_leitura=timezone.now(),
                    local=Local.objects.get(id=4)
                )

                messages.success(request, f'Tag {tag} vinculada a {pessoa}')
                return redirect('vincular_tag_pessoa')
            except (TagBle.DoesNotExist, Pessoa.DoesNotExist):
                messages.error(request, 'Tag ou pessoa indisponíveis. Tag não vinculada',)


    termo_busca = request.GET.get('busca')
    tags = TagBle.objects.filter(monitorado=None)[:3] #TODO remover quando em produção
    if termo_busca:
        resultados_da_busca = Pessoa.objects.filter(nome__icontains=termo_busca).order_by('id') | Pessoa.objects.filter(cpf__icontains=termo_busca).order_by('id')

    
    if resultados_da_busca:
        paginator = Paginator(resultados_da_busca, 5)  
        page_number = request.GET.get("page")
        resultados_da_busca_paginated = paginator.get_page(page_number)

    context = {

        'resultado': resultados_da_busca_paginated,
        'busca': termo_busca,
        'tags': tags #TODO remover quando em produção
    }
    return render(request, 'home/vincular_tag_pessoa.html', context)

@login_required(login_url='login')
def desvincular_tag_pessoa(request):
    if request.method == 'POST':
        # Obtenha o ID da tag do formulário enviado
        tag_id = request.POST.get('tagId')

        try:
            tag_ble = TagBle.objects.get(id=tag_id)
        except TagBle.DoesNotExist:
            messages.error(request, f'A tag {tag_id} não existe')
            return render(request, 'home/desvincular_tag_pessoa.html')



        try:
            pessoa = Pessoa.objects.get(tag_ble=tag_ble)
            if pessoa is not None:
                
                LeituraTag.objects.create(
                        tag_ble=pessoa.tag_ble,
                        raspberry=Raspberry.objects.get(id=5), #rasp = tag desvinculada
                        monitorado=pessoa,
                        data_leitura=timezone.now(),
                        local=Local.objects.get(id=3)
                ).save()
                
                pessoa.tag_ble = None
                pessoa.local_atual = Local.objects.get(id=3) #Local = tag desvinculada
                pessoa.save()

                


            messages.success(request, f'A tag {tag_id} foi desvinculada de {pessoa}')
        except:
            messages.error(request, f'A tag {tag_id} não está vinculada')


    return render(request, 'home/desvincular_tag_pessoa.html')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BleData

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
def recebe_dados_tag(request):
    if request.method == 'POST':
        try:
            data = request.POST
            mac_tag = data.get('mac_tag')
            rssi = int(data.get('rssi'))
            mac_raspberry = data.get('mac_raspberry')
            data_leitura = data.get('data_leitura')

            # Usar try-except para lidar com possíveis exceções de objeto não encontrado
            try:
                tag_ble = TagBle.objects.get(uuid_tag=mac_tag)
                raspberry = Raspberry.objects.get(uuid_rasp=mac_raspberry)
                monitorado = Monitorado.objects.get(tag_ble=tag_ble)
                local = Local.objects.get(raspberry=raspberry)
                leitura = None

                # Salvar os dados recebidos no banco de dados
                if monitorado.local_atual != local:
                    leitura = LeituraTag.objects.create(
                        tag_ble=tag_ble,
                        raspberry=raspberry,
                        monitorado=monitorado,
                        data_leitura=data_leitura,
                        local=local
                    )
                    if monitorado.local_atual != local:
                        monitorado.local_atual = local
                        monitorado.save()   

                print("Dados recebidos do Raspberry Pi:", leitura)
                return JsonResponse({'status': 'success'})
            except ObjectDoesNotExist as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)



#TODO criar MVT para cadastrar e listar objetos