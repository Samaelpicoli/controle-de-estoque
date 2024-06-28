from django import forms

from .models import Estoque, EstoqueItens


class EstoqueForm(forms.ModelForm):
    """
    Formulário para o modelo Estoque.

    Utiliza o ModelForm do Django para criar um formulário 
    baseado no modelo Estoque.
    """

    class Meta:
        model = Estoque
        # Inclui os campos funcionario e nf do modelo Estoque 
        # no formulário
        fields = ('funcionario', 'nf')


class EstoqueItensForm(forms.ModelForm):
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
