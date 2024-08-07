from django.urls import path

from produto import views


# Define o namespace para este conjunto de URLs
app_name = 'produto'

urlpatterns = [
    # URL para a view que lista todos os produtos
    path('', views.ProdutoList.as_view(), name='lista_produtos'),

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
    
    # URL para retornar os detalhes do produto em formato JSON
    path('<int:pk>/json/', views.produto_json, name='produto_json'),

    path('import/csv/', views.import_csv, name='import_csv'),

    path('export/csv/', views.export_csv, name='export_csv'),

    path('import/excel/', views.importar_xlsx, name='importar_xlsx'),
    
    path('export/excel', views.export_xlsx, name='export_xlsx'),

    path(
        'import/csv/pandas',
        views.import_csv_with_pandas,
        name='import_csv_with_pandas'
    )

]