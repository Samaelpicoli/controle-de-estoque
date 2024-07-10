from django.shortcuts import render

from django.views.generic import CreateView, UpdateView, ListView

from django.http import JsonResponse

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

    # Procura por um item no campo de busca
    search = request.GET.get('search')
    if search:
        objetos = objetos.filter(produto__icontains=search)
    
    # Define o contexto a ser passado para o template
    contexto = {'lista_objetos': objetos}

    # Renderiza o template com o contexto
    return render(request, template_name=nome_template, context=contexto)


class ProdutoList(ListView):
    """
    Classe-based view para listar produtos.
    
    Atributos:
        model (Model): O modelo que será utilizado na listagem.
        template_name (str): O nome do template que será renderizado.
        paginate_by (int): Quantidade de itens por página na paginação.
    """
    model = Produto
    template_name = 'lista_produtos.html'
    paginate_by = 10


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


def produto_json(request, pk):
    """
    Retorna os dados de um produto específico em formato JSON.

    Este método filtra o produto com base na chave primária 
    fornecida (pk), converte os dados principais do produto 
    em um formato de dicionário utilizando o método `dict_to_json`
    e retorna os dados como uma resposta JSON.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        pk (int): A chave primária do produto a ser recuperado.

    Returns:
        JsonResponse: Um objeto de resposta JSON contendo os 
        dados do produto.
    """
    produto = Produto.objects.filter(pk=pk)
    data = [item.dict_to_json() for item in produto]
    return JsonResponse({'data': data})