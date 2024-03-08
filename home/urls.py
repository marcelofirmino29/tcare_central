from django.urls import path
from home import views

urlpatterns = [
    # Define a rota raiz que corresponde à função 'index' no arquivo 'views.py' dentro do aplicativo 'home'
    path('',views.index, name='index'),
]



"""
Neste código:

urlpatterns é uma lista de objetos path que mapeiam URLs para funções de visualização (views).
path('', views.index, name='index') define a rota raiz do site, que corresponde à função de visualização index no arquivo views.py dentro do aplicativo home.
name='index' atribui um nome à rota, permitindo referenciar essa rota de forma única em todo o código Django. Isso é útil ao criar links em templates ou ao redirecionar para URLs internamente no código Python.
"""