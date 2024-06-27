from django.shortcuts import render, resolve_url

from django.forms import inlineformset_factory

from django.http import HttpResponseRedirect

from .models import Estoque, EstoqueItens

from .forms import EstoqueForm, EstoqueItensForm

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
    
    # Filtra os objetos do modelo Estoque onde movimento é 'e entrada'
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


def add_estoque_entrada(request):

    """
    View para adicionar uma nova entrada de estoque.

    Exibe um formulário para a criação de uma nova entrada de estoque
    e um formset para adicionar os itens do estoque. 
    Se o método da requisição for POST, valida e salva os dados do 
    formulário e do formset, redirecionando para a página de detalhes
    da entrada de estoque.

    Args:
        request (HttpRequest): Objeto HttpRequest que contém os 
        dados da requisição.

    Returns:
        HttpResponse: Renderiza o template com o formulário e o formset
        ou redireciona para a página de detalhes da entrada de estoque.
    """

    nome_template = 'form_estoque_entrada.html'
    
    # Instancia um novo objeto Estoque
    estoque_form = Estoque()

    # Define um formset para EstoqueItens relacionado ao Estoque
    item_estoque_formset = inlineformset_factory(
        Estoque,
        EstoqueItens,
        form = EstoqueItensForm,
        extra = 0,
        min_num = 1,
        validate_min = True,
    )

    if request.method == 'POST':
        # Se a requisição for POST, cria os formulários 
        # com os dados enviados
        form = EstoqueForm(
            request.POST, 
            instance=estoque_form, 
            prefix='main'
        )
        formset = item_estoque_formset(
            request.POST,
            instance = estoque_form,
            prefix = 'estoque'
        )

        # Verifica se os formulários são válidos
        if form.is_valid() and formset.is_valid():
            # Salva os formulários e redireciona 
            # para a página de detalhes da entrada de estoque
            form = form.save()
            formset.save()
            url = 'estoque:detalhes_estoque_entrada'
            return HttpResponseRedirect(resolve_url(url, form.pk))
    else:
        # Se a requisição não for POST, cria formulários vazios
        form = EstoqueForm(instance=estoque_form, prefix='main')
        formset = item_estoque_formset(
            instance=estoque_form, 
            prefix='estoque'
        )

    # Contexto passado para o template
    contexto = {'form': form, 'formset': formset}
    
    # Renderiza o template com os formulários
    return render(request, template_name=nome_template, context=contexto)