from datetime import datetime
from django.http import HttpResponse
import xlwt


def exportar_xlsx(model, filename, queryset, columns):
    """
    Exporta dados de um queryset para um arquivo Excel (.xlsx).

    Args:
        model (str): Nome do modelo cujos dados estão sendo exportados.
        filename (str): Nome do arquivo que será gerado.
        queryset (iterable): Conjunto de dados a serem exportados.
        columns (list): Lista de nomes de colunas a serem incluídas 
        no arquivo Excel.

    Returns:
        HttpResponse: Resposta HTTP com o conteúdo do arquivo Excel 
        para download.

    """
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(model)

    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    default_style = xlwt.XFStyle()

    rows = queryset

    for row, rowdata in enumerate(rows):
        row_num += 1
        for col, val in enumerate(rowdata):
            ws.write(row_num, col, val, default_style)
        
    wb.save(response)
    return response

