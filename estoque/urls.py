from django.urls import path

from estoque import views


app_name = 'estoque'

urlpatterns = [
    # URL para a view que lista todas as entradas do estoque.
    path('', views.lista_estoque_entrada, name='lista_estoque_entrada'),
    # URL para a view que lista os detalhes das entradas no estoque.
    path(
        '<int:pk>/detalhes/', 
        views.detalhes_estoque_entrada, 
        name='detalhes_estoque_entrada'
    ),
    # URL para a view que adiciona uma nova entrada no estoque.
    path('adicionar/', views.add_estoque_entrada, name='add_estoque_entrada'), 
    # URL para a view que lista todas as saídas do estoque.
    path('saida/', views.lista_estoque_saida, name='lista_estoque_saida'),
     # URL para a view que lista os detalhes das saídas no estoque.
    path(
        'saida/<int:pk>/detalhes', 
        views.detalhes_estoque_saida, 
        name='detalhes_estoque_saida'
    ),
    # URL para a view que adiciona uma nova saída no estoque.
    path('saida/add/', views.add_estoque_saida, name='add_estoque_saida'),

]