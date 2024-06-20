from django.shortcuts import render

from django.views.generic import CreateView, UpdateView

from .models import Produto

from .forms import ProdutoForm

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


def adicionar_produto(request):
    nome_template = 'formulario_produto.html'
    return render(request, template_name=nome_template)


class CriarProduto(CreateView):
    """
    View baseada em classe para criar um novo produto.

    Atributos:
        model (Model): O modelo que será utilizado na view.
        template_name (str): O nome do template que será renderizado.
        form_class (Form): O formulário que será utilizado 
        para criar o objeto.
    """
    model = Produto
    template_name = 'formulario_produto.html'
    form_class = ProdutoForm


class EditarProduto(UpdateView):
    """
    View baseada em classe para editar um produto.

    Atributos:
        model (Model): O modelo que será utilizado na view.
        template_name (str): O nome do template que será renderizado.
        form_class (Form): O formulário que será utilizado 
        para criar o objeto.
    """
    model = Produto
    template_name = 'formulario_produto.html'
    form_class = ProdutoForm