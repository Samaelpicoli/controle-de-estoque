from django.urls import path

from produto import views


# Define o namespace para este conjunto de URLs
app_name = 'produto'

urlpatterns = [
    # URL para a view que lista todos os produtos
    path('', views.lista_produtos, name='lista_produtos'),
    # URL para a view de detalhe de um produto específico
    path('<int:pk>/', views.detalhe_produto, name='detalhe_produto'),

]