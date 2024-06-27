from django.contrib import admin

from .models import EstoqueEntrada, EstoqueSaida, EstoqueItens

# Register your models here.


class EstoqueItensInline(admin.TabularInline):
    """
    Inline admin para itens de estoque, permitindo edição direta
    na página de administração de Estoque.

    Attributes:
        model (Model): Modelo relacionado ao inline.
        extra (int): Número de linhas extras a serem exibidas.
    """
    model = EstoqueItens
    extra = 0


# Decorador que registra o modelo Estoque Entrada
# com o site de administração do Django.
@admin.register(EstoqueEntrada)
class EstoqueEntradaAdmin(admin.ModelAdmin):
    """
    Configurações de administração para o modelo Estoque.

    Attributes:
        list_display (tuple): Campos a serem exibidos na lista 
        de registros de Estoque.

        search_fields (tuple): Campos a serem usados na pesquisa 
        do admin.

        list_filter (tuple): Campos a serem usados para filtragem 
        no admin.

        date_hierarchy (str): Campo a ser usado para navegação por
        data no admin.
    
        inlines (list): Lista de classes Inline para exibir na página
        de administração de Estoque.
    """
    inlines = (EstoqueItensInline,)
    list_display = ('__str__', 'nf', 'funcionario',)
    search_fields = ('nf',)
    list_filter = ('funcionario', )
    date_hierarchy = 'criado_em'



# Decorador que registra o modelo Estoque Saida
# com o site de administração do Django.
@admin.register(EstoqueSaida)
class EstoqueSaidaAdmin(admin.ModelAdmin):
    """
    Configurações de administração para o modelo Estoque.

    Attributes:
        list_display (tuple): Campos a serem exibidos na lista 
        de registros de Estoque.

        search_fields (tuple): Campos a serem usados na pesquisa 
        do admin.

        list_filter (tuple): Campos a serem usados para filtragem 
        no admin.

        date_hierarchy (str): Campo a ser usado para navegação por
        data no admin.
    
        inlines (list): Lista de classes Inline para exibir na página
        de administração de Estoque.
    """
    inlines = (EstoqueItensInline,)
    list_display = ('__str__', 'nf', 'funcionario',)
    search_fields = ('nf',)
    list_filter = ('funcionario', )
    date_hierarchy = 'criado_em'
    