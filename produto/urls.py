from django.urls import path

from produto import views


# Define o namespace para este conjunto de URLs
app_name = 'produto'

urlpatterns = [
    # URL para a view que lista todos os produtos
    path('', views.lista_produtos, name='lista_produtos'),
    # URL para a view de detalhe de um produto específico
    path('<int:pk>/', views.detalhe_produto, name='detalhe_produto'),
    # URL para a view de formulário para adicionar um novo produto
    # com uma classe, utilizo o método as_view() para a chamada
    path('adicionar/', views.CriarProduto.as_view(), name='adicionar_produto'),
    # URL para editar um produto, com classe based views
    path(
        '<int:pk>/editar/', 
        views.EditarProduto.as_view(),
        name='editar_produto'
    ),

]