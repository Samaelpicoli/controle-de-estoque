from django.shortcuts import render, resolve_url

from django.forms import inlineformset_factory

from django.http import HttpResponseRedirect

from produto.models import Produto

from .models import EstoqueEntrada, EstoqueSaida, EstoqueItens, Estoque

from .forms import EstoqueForm, EstoqueItensForm

# Create your views here.

def lista_estoque_entrada(request):
    """
    View para listar as entradas de estoque.

    Esta função consulta todas as instâncias de EstoqueEntrada 
    e as passa para o template 'lista_estoque_entrada.html' 
    para renderização.

    Args:
        request (HttpRequest): O objeto de solicitação HTTP.

    Returns:
        HttpResponse: A resposta HTTP com o template renderizado.
    """
    # Nome do template a ser renderizado
    nome_template = 'lista_estoque_entrada.html'
    
    # Filtra os objetos do modelo Estoque onde movimento é 'e entrada'
    objetos = EstoqueEntrada.objects.all()
    
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
    obj = EstoqueEntrada.objects.get(pk=pk)

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
        EstoqueEntrada,
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

            # Chama a função para atualizar o estoque dos 
            # produtos com base nos dados do formulário
            baixa_no_estoque(form)

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


def baixa_no_estoque(form):
    """
    Atualiza o estoque dos produtos com base nas entradas 
    fornecidas no form.

    Esta função percorre todos os itens do estoque presentes
    no formulário, atualiza a quantidade em estoque de cada 
    produto correspondente e salva as alterações no banco de dados.

    Args:
        form: formulário de entrada de estoque
        contendo os itens de estoque.
    """

    # Obtém todos os itens de estoque associados ao formulário
    produtos = form.estoques.all()

    # Itera sobre cada item do estoque
    for item in produtos:

        # Obtém o produto correspondente usando a chave primária
        produto = Produto.objects.get(pk=item.produto.pk)

        # Atualiza a quantidade em estoque do produto
        produto.estoque = item.saldo

        # Salva no Banco de dados
        produto.save()
    print('Estoque atualizado')


def lista_estoque_saida(request):
    """
    View para listar as saídas de estoque.

    Esta função consulta todas as instâncias de EstoqueSaida 
    e as passa para o template 'lista_estoque_saida.html' 
    para renderização.

    Args:
        request (HttpRequest): O objeto de solicitação HTTP.

    Returns:
        HttpResponse: A resposta HTTP com o template renderizado.
    """
    # Nome do template a ser renderizado
    nome_template = 'lista_estoque_saida.html'
    
    # Consulta todas as instâncias de EstoqueSaida
    objetos = EstoqueSaida.objects.all()
    
    # Contexto a ser passado para o template
    contexto = {'objetos': objetos}
    
    # Renderiza o template com o contexto
    return render(request, template_name=nome_template, context=contexto)


def detalhes_estoque_saida(request, pk):

    """
    View para exibir os detalhes de uma saída de estoque específica.

    Esta função busca um objeto do modelo Estoque usando a 
    chave primária (pk) fornecida e renderiza o template 
    'detalhes_estoque_saida.html' com esse objeto no contexto.

    Args:
        request (HttpRequest): O objeto de solicitação HTTP.
        pk (int): A chave primária do objeto Estoque a ser detalhado.

    Returns:
        HttpResponse: A resposta HTTP com o template renderizado.
    """

    # Nome do template a ser renderizado
    nome_template = 'detalhes_estoque_saida.html'

    # Busca o objeto Estoque usando a chave primária (pk) fornecida
    obj = EstoqueSaida.objects.get(pk=pk)

    # Contexto a ser passado para o template
    contexto = {'objeto': obj}

    # Renderiza o template com o contexto
    return render(request, template_name=nome_template, context=contexto)


def add_estoque_saida(request):
    """
    View para adicionar uma nova saida de estoque.

    Exibe um formulário para a criação de uma nova saida de estoque
    e um formset para adicionar os itens do estoque. 
    Se o método da requisição for POST, valida e salva os dados do 
    formulário e do formset, redirecionando para a página de detalhes
    da saida de estoque.

    Args:
        request (HttpRequest): Objeto HttpRequest que contém os 
        dados da requisição.

    Returns:
        HttpResponse: Renderiza o template com o formulário e o formset
        ou redireciona para a página de detalhes da saida de estoque.
    """

    nome_template = 'form_estoque_saida.html'
    
    # Instancia um novo objeto Estoque
    estoque_form = Estoque()

    # Define um formset para EstoqueItens relacionado ao Estoque
    item_estoque_formset = inlineformset_factory(
        EstoqueSaida,
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

            # Chama a função para atualizar o estoque dos 
            # produtos com base nos dados do formulário
            baixa_no_estoque(form)

            url = 'estoque:detalhes_estoque_saida'
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

