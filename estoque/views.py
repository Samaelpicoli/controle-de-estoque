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
    
    # Filtra os objetos do modelo Estoque onde movimento 'e' (entrada)
    objetos = Estoque.objects.filter(movimento='e')
    
    # Contexto a ser passado para o template
    contexto = {'objetos': objetos}
    
    # Renderiza o template com o contexto
    return render(request, template_name=nome_template, context=contexto)
