import xlrd

from ..models import Categoria, Produto


def importar_xlsx(filename):
    """
    Importa dados de um arquivo Excel (.xlsx) e os salva no 
    banco de dados.

    Args:
        filename (str): O caminho para o arquivo Excel a ser importado.

    """
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_index(0)
    fields = (
        'produto', 'ncm', 'importado', 'preco', 'estoque', 'estoque_minimo'
    )
    categorias = []
    for row in range(1, sheet.nrows):
        categoria = sheet.row(row)[6].value
        categorias.append(categoria)
    categorias_unicas = [Categoria(categoria=categoria)
                        for categoria in set(categorias) if categoria]
    Categoria.objects.bulk_create(categorias_unicas)
    aux = []
    for row in range(1, sheet.nrows):
        produto = sheet.row(row)[0].value
        ncm = str(sheet.row(row)[1].value)
        _importado = sheet.row(row)[2].value
        importado = True if _importado == 'True' else False
        preco = sheet.row(row)[3].value
        estoque = sheet.row(row)[4].value
        estoque_minimo = sheet.row(row)[5].value
        _categoria = sheet.row(row)[6].value
        categoria = Categoria.objects.filter(categoria=_categoria).first()
        produto = dict(
            produto=produto,
            ncm=ncm,
            importado=importado,
            preco=preco,
            estoque=estoque,
            estoque_minimo=estoque_minimo,
        )
        if categoria:
            obj = Produto(categoria=categoria, **produto)
        else:
            obj = Produto(**produto)
        aux.append(obj)
    Produto.objects.bulk_create(aux)


