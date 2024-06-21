from django.urls import path

from estoque import views


app_name = 'estoque'

urlpatterns = [
    # URL para a view que lista todas as entradas do estoque.
    path('', views.lista_estoque_entrada, name='lista_estoque_entrada'),
    #URL para a view que lista os detalhes das entradas no estoque.
    path(
        '<int:pk>/detalhes/', 
        views.detalhes_estoque_entrada, 
        name='detalhes_estoque_entrada'
    ),

    
]