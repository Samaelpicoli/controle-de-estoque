from django import forms

from .models import Estoque, EstoqueItens
from produto.models import Produto


class EstoqueForm(forms.ModelForm):
    """
    Formulário para o modelo Estoque.

    Utiliza o ModelForm do Django para criar um formulário 
    baseado no modelo Estoque.
    """

    class Meta:
        model = Estoque
        # Inclui os campo de nf do modelo Estoque 
        # no formulário
        fields = ('nf',)


class EstoqueItensSaidaForm(forms.ModelForm):
    """
    Formulário para o modelo EstoqueItens.

    Utiliza o ModelForm do Django para criar um 
    formulário baseado no modelo EstoqueItens.
    """

    class Meta:
        model = EstoqueItens
        # Inclui todos os campos do modelo EstoqueItens
        # no formulário
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        Filtro para ficar disponível para saída do estoque
        somente produtos com mais itens do que 0.
        """
        super(EstoqueItensSaidaForm, self).__init__(*args, **kwargs)
        self.fields['produto'].queryset = Produto.objects.filter(estoque__gt=0)


class EstoqueItensEntradaForm(forms.ModelForm):
    """
    Formulário para o modelo EstoqueItens.

    Utiliza o ModelForm do Django para criar um 
    formulário baseado no modelo EstoqueItens.
    """

    class Meta:
        model = EstoqueItens
        # Inclui todos os campos do modelo EstoqueItens
        # no formulário
        fields = '__all__'