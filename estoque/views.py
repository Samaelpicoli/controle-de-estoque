from django.contrib.auth.decorators import login_required

from django.shortcuts import render, resolve_url

from django.forms import inlineformset_factory

from django.http import HttpResponseRedirect

from django.views.generic import ListView, DetailView

from produto.models import Produto

from .models import EstoqueEntrada, EstoqueSaida, EstoqueItens, Estoque

from .forms import EstoqueForm, EstoqueItensForm

# Create your views here.

def add_estoque(request, template_name, movimento, url):
    """
    Adiciona uma nova entrada ou saída de estoque.

    Esta função cria um novo formulário e um formset para itens 
    de estoque. Se a requisição for POST, ela valida e 
    salva os formulários, atualiza o estoque dos produtos e 
    redireciona para a página de detalhes do estoque.

    Args:
        request (HttpRequest): O objeto de solicitação HTTP.
        template_name (str): O nome do template a ser renderizado.
        movimento (str): O tipo de movimento de estoque 
        ('e' para entrada, 's' para saída).
        url (str): A URL para redirecionamento após salvar 
        os formulários.

    Returns:
        dict: Contexto contendo os formulários e formset, ou 
        redireciona para a página de detalhes do estoque.
    """
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
            # Salva os formulário
            form = form.save()
            # Define o tipo de movimento de estoque (entrada ou saída)
            form.movimento = movimento
            form.save()
            # Salva o formset de itens de estoque
            formset.save()

            # Chama a função para atualizar o estoque dos 
            # produtos com base nos dados do formulário
            baixa_no_estoque(form)
            return {'pk': form.pk}
    else:
        # Se a requisição não for POST, cria formulários vazios
        form = EstoqueForm(instance=estoque_form, prefix='main')
        formset = item_estoque_formset(
            instance=estoque_form, 
            prefix='estoque'
        )
    # Cria o contexto a ser passado para o template
    contexto = {'form': form, 'formset': formset}
    return contexto

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
    nome_template = 'lista_estoque.html'
    
    # Filtra os objetos do modelo Estoque onde movimento é 'e entrada'
    objetos = EstoqueEntrada.objects.all()
    
    # Contexto a ser passado para o template
    contexto = {
        'objetos': objetos, 
        'titulo': 'Entrada',
        'url_add': 'estoque:add_estoque_entrada'
    }
    
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
    nome_template = 'detalhes_estoque.html'

    # Busca o objeto Estoque usando a chave primária (pk) fornecida
    obj = EstoqueEntrada.objects.get(pk=pk)

    # Contexto a ser passado para o template
    contexto = {
        'objeto': obj,
        'url_lista': 'estoque:lista_estoque_entrada'
    }

    # Renderiza o template com o contexto
    return render(request, template_name=nome_template, context=contexto)


@login_required
def add_estoque_entrada(request):
    """
    Adiciona uma nova entrada de estoque.

    Esta função utiliza a função add_estoque para criar e validar os
    formulários de entrada de estoque. Se os formulários forem válidos
    e os dados forem salvos, redireciona para a página de detalhes da 
    entrada de estoque.

    Args:
    request (HttpRequest): O objeto de solicitação HTTP.

    Returns:
        HttpResponse: Redireciona para a página de detalhes da entrada de
        estoque se os dados forem salvos, caso contrário, renderiza o 
        template com os formulários.
    """

    nome_template = 'form_estoque_entrada.html'
    
    # Define o tipo de movimento como 'entrada'
    movimento = 'e'

    # URL de redirecionamento após salvar os dados
    url = 'estoque:detalhes_estoque'

    # Contexto passado para o template
    contexto = add_estoque(request, nome_template, movimento, url)

     # Verifica se a chave 'pk' está presente no contexto 
     # (indicando que os dados foram salvos)
    if contexto.get('pk'):
        # Redireciona para a página de detalhes da entrada de estoque
        return HttpResponseRedirect(resolve_url(url, contexto.get('pk')))
    
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
    nome_template = 'lista_estoque.html'
    
    # Consulta todas as instâncias de EstoqueSaida
    objetos = EstoqueSaida.objects.all()
    
    # Contexto a ser passado para o template
    contexto = {
        'objetos': objetos, 
        'titulo': 'Entrada',
        'url_add': 'estoque:add_estoque_saida'
    }
    
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
    nome_template = 'detalhes_estoque.html'

    # Busca o objeto Estoque usando a chave primária (pk) fornecida
    obj = EstoqueSaida.objects.get(pk=pk)

    # Contexto a ser passado para o template
    contexto = {
        'objeto': obj,
        'url_lista': 'estoque:lista_estoque_entrada'
    }

    # Renderiza o template com o contexto
    return render(request, template_name=nome_template, context=contexto)


@login_required
def add_estoque_saida(request):
    """
    Adiciona uma nova saída de estoque.

    Esta função utiliza a função add_estoque para criar e validar os
    formulários de saída de estoque. Se os formulários forem válidos
    e os dados forem salvos, redireciona para a página de detalhes da 
    saída de estoque.

    Args:
    request (HttpRequest): O objeto de solicitação HTTP.

    Returns:
        HttpResponse: Redireciona para a página de detalhes da saída de
        estoque se os dados forem salvos, caso contrário, renderiza o 
        template com os formulários.
    """
    
    nome_template = 'form_estoque_saida.html'
    
    # Define o tipo de movimento como saída
    movimento = 's'

    # URL de redirecionamento após salvar os dados
    url = 'estoque:detalhes_estoque'

    # Contexto passado para o template
    contexto = add_estoque(request, nome_template, movimento, url)

    # Verifica se a chave 'pk' está presente no contexto 
    # (indicando que os dados foram salvos)
    if contexto.get('pk'):
        # Redireciona para a página de detalhes da saída de estoque
        return HttpResponseRedirect(resolve_url(url, contexto.get('pk')))
    
    # Renderiza o template com os formulários
    return render(request, template_name=nome_template, context=contexto)


class ListaEstoqueEntrada(ListView):
    """
    Classe-based view para listar as entradas de estoque.
    """
    model = EstoqueEntrada
    template_name = 'lista_estoque.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        """
        Adiciona dados adicionais ao contexto do template.

        Returns:
            dict: Contexto atualizado com título e URL 
            para adicionar entrada de estoque.
        """
        context = super(ListaEstoqueEntrada, self).get_context_data(**kwargs)
        context['titulo'] = 'Entrada'
        context['url_add'] = 'estoque:add_estoque_entrada'
        return context
    

class ListaEstoqueSaida(ListView):
    """
    Classe-based view para listar as saídas de estoque.
    """
    # Define o modelo a ser usado para listar os objetos
    model = EstoqueSaida

    # Define o template a ser renderizado
    template_name = 'lista_estoque.html'  

    def get_context_data(self, **kwargs):
        """
        Adiciona dados adicionais ao contexto do template.

        Returns:
            dict: Contexto atualizado com título e URL para adicionar
            saída de estoque.
        """
        # Chama o método get_context_data da superclasse 
        # para obter o contexto padrão
        context = super(ListaEstoqueSaida, self).get_context_data(**kwargs)
        context['titulo'] = 'Saída'
        context['url_add'] = 'estoque:add_estoque_saida'
        return context
    
    
class DetalheEstoque(DetailView):
    """
    Classe-based view para exibir os detalhes de uma entrada ou 
    saída no estoque.

    Atributos:
        model (class): O modelo que será utilizado pela view. 
        Neste caso, é o modelo `Estoque`.
        template_name (str): O nome do template que será utilizado 
        para renderizar a página de detalhes.
    """
    model = Estoque
    template_name = 'detalhes_estoque.html'

