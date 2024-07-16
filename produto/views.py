import csv
from datetime import datetime
import io

from django.contrib import messages
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
import pandas as pd

from .models import Produto
from .forms import ProdutoForm
from produto.actions.import_xlsx import importar_xlsx as actions_importar_xlsx
from produto.actions.export_xlsx import exportar_xlsx as actions_exportar_xlsx

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


def save_data(data):
    '''
    Salva os dados no banco.
    
    Args:
        data (list): Uma lista de OrderedDicts com os dados do CSV.
    '''
    aux = []
    for item in data:
        produto = item.get('produto')
        ncm = str(item.get('ncm'))
        importado = True if item.get('importado') == 'True' else False
        preco = item.get('preco')
        estoque = item.get('estoque')
        estoque_minimo = item.get('estoque_minimo')
        obj = Produto(
            produto=produto,
            ncm=ncm,
            importado=importado,
            preco=preco,
            estoque=estoque,
            estoque_minimo=estoque_minimo,
        )
        aux.append(obj)
    Produto.objects.bulk_create(aux)


def import_csv(request):
    """
    View para importar dados de um arquivo CSV e salvar no 
    banco de dados.

    Esta view processa o upload de um arquivo CSV contendo 
    dados de produtos, lê o conteúdo do arquivo, converte os dados em 
    um formato adequado e salva os dados no banco de dados.

    Args:
        request (HttpRequest): O objeto da requisição HTTP.

    Returns:
        HttpResponse: Se a requisição for POST e o arquivo for enviado,
        redireciona para a lista de produtos após salvar os dados.
        Se a requisição não for POST, renderiza o template de 
        upload de arquivo.
    """

    if request.method == 'POST' and request.FILES['myfle']:
        # Lê o arquivo enviado
        myfile = request.FILES['myfile']
        file = myfile.read().decode('utf-8')
        
        # Converte o conteúdo do arquivo em um DictReader
        reader = csv.DictReader(io.StringIO(file))
        
        # Cria uma lista de dicionários a partir do conteúdo do CSV
        data = [linha for linha in reader]
        
        # Salva os dados no banco de dados
        save_data(data)
        
        # Redireciona para a lista de produtos após salvar os dados
        return HttpResponseRedirect(reverse('produto:lista_produtos'))
    
    # Renderiza o template de upload de arquivo se a requisição não 
    # for POST
    template_name = 'import_produto.html'
    return render(request, template_name)


def export_csv(request):
    """
    Exporta dados de produtos para um arquivo CSV.

    Este método obtém todos os produtos do banco de dados e escreve
    suas informações em um arquivo CSV. Após a exportação, uma mensagem
    de sucesso é adicionada e o usuário é redirecionado para a lista de
    produtos.

    Args:
        request (HttpRequest): O objeto de solicitação HTTP.

    Returns:
        HttpResponseRedirect: Redireciona para a página de lista de 
        produtos após a exportação bem-sucedida.
    """

    header = (
        'importado', 'ncm', 'produto', 'preco', 'estoque', 'estoque_minimo',
    )

    # Obtém todos os produtos do banco de dados, selecionando 
    # apenas os campos definidos no cabeçalho
    produtos = Produto.objects.all().values_list(*header)
    with open('fix/produtos_exportados.csv', 'w') as csvfile:
        produto_writer = csv.writer(csvfile)
        produto_writer.writerow(header)
        for produto in produtos:
            produto_writer.writerow(produto)

    # Adiciona uma mensagem de sucesso para ser exibida ao usuários
    messages.success(request, 'Produtos exportados com sucesso.')
    return HttpResponseRedirect(reverse('produto:lista_produtos'))


def importar_xlsx(request):
    """
    View para importar produtos de um arquivo XLSX.

    Lê um arquivo XLSX contendo dados de produtos e salva esses 
    dados no banco de dados.

    Args:
        request (HttpRequest): A solicitação HTTP recebida pelo 
        servidor.

    Returns:
        HttpResponseRedirect: Redireciona o usuário para a lista 
        de produtos após a importação bem-sucedida.
    """
    filename = 'fix/produtos.xlsx'
    actions_importar_xlsx(filename)
    messages.success(request, 'Produtos importados com sucesso.')
    return HttpResponseRedirect(reverse('produto:lista_produtos'))


def export_xlsx(request):
    """
    View para exportar produtos para um arquivo XLSX.

    Gera um arquivo XLSX contendo dados de produtos e o envia 
    como resposta HTTP para download.

    Args:
        request (HttpRequest): A solicitação HTTP recebida pelo 
        servidor.

    Returns:
        HttpResponse: Resposta HTTP contendo o arquivo XLSX para 
        download.
    """
    data = datetime.now().strftime('%Y-%m-%d')
    model = 'Produto'
    filename = 'produtos_exportados.xlsx'
    _filename = filename.split('.')
    filename_final = f'{_filename[0]}_{data}.{_filename[1]}'

    # Obtem os dados dos produtos a serem exportados
    queryset = Produto.objects.all().values_list(
        'importado',
        'ncm',
        'produto',
        'preco',
        'estoque',
        'estoque_minimo',
        'categoria__categoria'
    )

    # Define as colunas do arquivo XLSX
    columns = (
        'Importado', 
        'NCM', 
        'Produto', 
        'Preço', 
        'Estoque', 
        'Estoque Minimo', 
        'Categoria'
    )

    # Gera a resposta HTTP com o arquivo XLSX
    response = actions_exportar_xlsx(model, filename_final, queryset, columns)
    return response


def import_csv_with_pandas(request):
    filename = 'fix/produtos.csv'
    df = pd.read_csv(filename)
    aux = []
    for row in df.values:
        obj = Produto(
            produto=row[0],
            ncm = row[1],
            importado = row[2],
            preco = row[3],
            estoque = row[4],
            estoque_minimo = row[5]
        )
        aux.append(obj)
    Produto.objects.bulk_create(aux)
    messages.success(request, 'Produtos importados com sucesso.')
    return HttpResponseRedirect(reverse('produto:lista_produtos'))