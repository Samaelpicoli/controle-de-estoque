from django.shortcuts import render

from .models import Estoque

# Create your views here.

def lista_estoque_entrada(request):
    """
    View para listar as entradas de estoque.

    Esta função busca todos os objetos do modelo Estoque onde o campo 
    'movimento' é igual a 'e' (entrada) e renderiza o template 
    'lista_estoque_entrada.html' com esses objetos.

    Args:
        request (HttpRequest): O objeto de solicitação HTTP.

    Returns:
        HttpResponse: A resposta HTTP com o template renderizado.
    """
    # Nome do template a ser renderizado
    nome_template = 'lista_estoque_entrada.html'
    
    # Filtra os objetos do modelo Estoque onde movimento é 'e' (entrada)
    objetos = Estoque.objects.filter(movimento='e')
    
    # Contexto a ser passado para o template
    contexto = {'objetos': objetos}
    
    # Renderiza o template com o contexto
    return render(request, template_name=nome_template, context=contexto)


def detalhes_estoque_entrada(request, pk):

    """
    View para exibir os detalhes de uma entrada de estoque específica.

    Esta função busca um objeto do modelo Estoque usando a 
    chave primária (pk) fornecida e renderiza o template 
    'detalhes_estoque_entrada.html' com esse objeto no contexto.

    Args:
        request (HttpRequest): O objeto de solicitação HTTP.
        pk (int): A chave primária do objeto Estoque a ser detalhado.

    Returns:
        HttpResponse: A resposta HTTP com o template renderizado.
    """

    # Nome do template a ser renderizado
    nome_template = 'detalhes_estoque_entrada.html'

    # Busca o objeto Estoque usando a chave primária (pk) fornecida
    obj = Estoque.objects.get(pk=pk)

    # Contexto a ser passado para o template
    contexto = {'objeto': obj}

    # Renderiza o template com o contexto
    return render(request, template_name=nome_template, context=contexto)