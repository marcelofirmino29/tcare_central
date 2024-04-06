from django.urls import path
from home import views

urlpatterns = [
    # Define a rota raiz que corresponde à função 'index' no arquivo 'views.py' dentro do aplicativo 'home'
    path('',views.index, name='index'),
    path('tags/',views.tags, name='tags'),
    path('cadastrar_tag/',views.cadastrar_tag, name='cadastrar_tag'),
    path('vincular_tag_pessoa/',views.vincular_tag_pessoa, name='vincular_tag_pessoa'),
    path('pessoas/',views.pessoas, name='pessoas'),
    path('cadastrar_paciente/',views.cadastrar_paciente, name='cadastrar_paciente'),
    path('cadastrar_acompanhante/',views.cadastrar_acompanhante, name='cadastrar_acompanhante'),
    path('cadastrar_funcionario/',views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('simula_leitura/',views.simula_leitura, name='simula_leitura'),
    path('leituras/',views.leituras, name='leituras'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('local/<str:local_localizacao>/',views.local_detalhes, name='local_detalhes'),
    path('locais_por_tipo/',views.locais_por_tipo, name='locais_por_tipo'),

    # user
    path('usuario/registrar/',views.registrar_usuario, name='registrar_usuario'),
    path('usuario/login/',views.login_view, name='login'),
    path('usuario/logout/',views.logout_view, name='logout'),

]



"""
Neste código:

urlpatterns é uma lista de objetos path que mapeiam URLs para funções de visualização (views).
path('', views.index, name='index') define a rota raiz do site, que corresponde à função de visualização index no arquivo views.py dentro do aplicativo home.
name='index' atribui um nome à rota, permitindo referenciar essa rota de forma única em todo o código Django. Isso é útil ao criar links em templates ou ao redirecionar para URLs internamente no código Python.
"""