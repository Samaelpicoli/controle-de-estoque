from django.urls import path, include

from estoque import views


app_name = 'estoque'


entrada_patterns = [
    # URL para a view que lista todas as entradas do estoque.
    path(
        '', 
        views.ListaEstoqueEntrada.as_view(), 
        name='lista_estoque_entrada'
    ),


    # URL para a view que adiciona uma nova entrada no estoque.
    path('adicionar/', views.add_estoque_entrada, name='add_estoque_entrada'),
]


saida_patterns = [
    # URL para a view que lista todas as saídas do estoque.
    path(
        '', 
        views.ListaEstoqueSaida.as_view(), 
        name='lista_estoque_saida'
    ),

    # URL para a view que adiciona uma nova saída no estoque.
    path('add/', views.add_estoque_saida, name='add_estoque_saida'),
]


urlpatterns = [
    # URL para a view que lista os detalhes das saidas no estoque.
    path(
        '<int:pk>/detalhes/', 
        views.DetalheEstoque.as_view(), 
        name='detalhes_estoque'
    ),
    path('entrada/', include(entrada_patterns)),
    path('saida/', include(saida_patterns)),
]