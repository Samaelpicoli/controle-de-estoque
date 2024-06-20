from django.shortcuts import render

from .models import Produto

# Create your views here.

def lista_produtos(request):
    """
    View para listar todos os produtos.
    
    Args:
        request (HttpRequest): O objeto de solicitação HTTP.

    Returns:
        HttpResponse: A resposta HTTP com o template 
        `lista_produtos.html` renderizado.
    """
    nome_template = 'lista_produtos.html'

    # Recupera todos os objetos do modelo Produto
    objetos = Produto.objects.all()
    
    # Define o contexto a ser passado para o template
    contexto = {'lista_objetos': objetos}

    # Renderiza o template com o contexto
    return render(request, template_name=nome_template, context=contexto)



def detalhe_produto(request, pk):
    """
    View para exibir os detalhes de um produto específico.
    
    Args:
        request (HttpRequest): O objeto de solicitação HTTP.
        pk (int): A chave primária do produto a ser exibido.

    Returns:
        HttpResponse: A resposta HTTP com o template 
        `detalhe_produto.html` renderizado.
    """
    nome_template = 'detalhe_produto.html'

    # Recupera o objeto Produto com a chave primária fornecida
    obj = Produto.objects.get(pk=pk)
    
    # Define o contexto a ser passado para o template
    contexto = {'objeto': obj}

    # Renderiza o template com o contexto
    return render(request, template_name=nome_template, context=contexto)