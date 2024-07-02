from django.urls import path

from estoque import views


app_name = 'estoque'

urlpatterns = [
    # URL para a view que lista todas as entradas do estoque.
    path(
        '', 
        views.ListaEstoqueEntrada.as_view(), 
        name='lista_estoque_entrada'
    ),

    # URL para a view que lista os detalhes das entradas no estoque.
    path(
        '<int:pk>/detalhes/', 
        views.DetalheEstoqueEntrada.as_view(), 
        name='detalhes_estoque_entrada'
    ),

    # URL para a view que adiciona uma nova entrada no estoque.
    path('adicionar/', views.add_estoque_entrada, name='add_estoque_entrada'),

    # URL para a view que lista todas as saídas do estoque.
    path(
        'saida/', 
        views.ListaEstoqueSaida.as_view(), 
        name='lista_estoque_saida'
    ),

     # URL para a view que lista os detalhes das saídas no estoque.
    path(
        'saida/<int:pk>/detalhes', 
        views.DetalheEstoqueSaida.as_view(), 
        name='detalhes_estoque_saida'
    ),
    
    # URL para a view que adiciona uma nova saída no estoque.
    path('saida/add/', views.add_estoque_saida, name='add_estoque_saida'),

]