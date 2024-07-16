import csv
from datetime import datetime
import xlwt
from django.contrib import admin
from django.http import HttpResponse
from .models import Categoria, Produto

# Register your models here.
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    """
    Configura a interface de administração do Django para o modelo 
    Produto.

    Attributes:
        list_display (tuple): Campos a serem exibidos na 
        listagem do modelo.

        search_fields (tuple): Campos pelos quais a pesquisa pode 
        ser feita.

        list_filter (tuple): Campos pelos quais a lista pode ser 
        filtrada.
    """
    
    list_display = (
        '__str__',
        'importado',
        'ncm',
        'preco',
        'estoque',
        'estoque_minimo',
        'categoria',
    )

    search_fields = ('produto',)

    list_filter = ('importado',)

    actions = ('export_as_csv', 'export_as_xlsx')

    class Media:
        js = (
            'https://code.jquery.com/jquery-3.3.1.min.js',
            '/static/js/estoque_admin.js'
        )

    def export_as_csv(self, request, queryset):
        """
        Exporta os produtos selecionados como um arquivo CSV.

        Args:
            request: Objeto HttpRequest.
            queryset: Conjunto de objetos selecionados na interface 
            de administração.
        
        Returns:
            HttpResponse: Resposta HTTP contendo o arquivo CSV para 
            download.
        """
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        # Configura a resposta HTTP com o tipo de conteúdo e o cabeçalho 
        # de disposição de conteúdo.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)

        # Cria um escritor CSV e escreve a linha de cabeçalho
        # com os nomes dos campos.
        writer = csv.writer(response)
        writer.writerow(field_names)

        # Itera sobre o conjunto de objetos e escreve os valores 
        # dos campos em cada linha.
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response
    
    export_as_csv.short_description = 'Exportar CSV'

    def export_as_xlsx(self, request, queryset):
        """
        Exporta os produtos selecionados como um arquivo XLSX.

        Args:
            request: Objeto HttpRequest.
            queryset: Conjunto de objetos selecionados na interface 
            de administração.
        
        Returns:
            HttpResponse: Resposta HTTP contendo o arquivo XLSX 
            para download.
        """
        meta = self.model._meta
        columns = (
            'Importado', 
            'NCM', 
            'Produto', 
            'Preço', 
            'Estoque', 
            'Estoque Minimo', 
            'Categoria'
        )
        data = datetime.now().strftime('%Y-%m-%d')

        # Configura a resposta HTTP com o tipo de conteúdo e 
        # o cabeçalho de disposição de conteúdo.
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="%s_%s.xlsx"' % (meta, data)

        # Cria um novo workbook e uma nova folha.
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(self.model.__name__)

        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        # Escreve os nomes das colunas na primeira linha com 
        # estilo em negrito.
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        
        default_style = xlwt.XFStyle()
        # Obtém os valores dos campos dos objetos selecionados.
        rows = queryset.values_list(
            'importado',
            'ncm',
            'produto',
            'preco',
            'estoque',
            'estoque_minimo',
            'categoria__categoria'
        )

        # Itera sobre as linhas e os dados das linhas, 
        # escrevendo-os na folha.
        for row, rowdata in enumerate(rows):
            row_num += 1
            for col, val in enumerate(rowdata):
                ws.write(row_num, col, val, default_style)
            
        # Salva o workbook na resposta HTTP.
        wb.save(response)
        return response

    export_as_xlsx.short_description = 'Exportar XLSX'


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """
    Configura a interface de administração do Django para o modelo 
    Categoria.

    Attributes:
        list_display (tuple): Campos a serem exibidos na listagem 
        do modelo.
        search_fields (tuple): Campos pelos quais a pesquisa pode 
        ser feita.
        list_filter (tuple): Campos pelos quais a lista pode ser 
        filtrada.
    """
    list_display = ('__str__',)
    search_fields = ('categoria',)
