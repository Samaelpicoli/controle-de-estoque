from django.db import models

from django.contrib.auth.models import User

from core.models import TimeStampModel

from produto.models import Produto

# Create your models here.

# Define os tipos de movimento de estoque.
MOVIMENTO = (
    ('e', 'entrada'),
    ('s', 'saida')
)

class Estoque(TimeStampModel):
    """
    Modelo que representa um registro de movimento de estoque.

    Attributes:
        funcionario (ForeignKey): Referência para o usuário 
        (funcionário) que realizou o movimento de estoque.
        nf (PositiveIntegerField): Número da Nota Fiscal, 
        opcional.
        movimento (CharField): Tipo de movimento de estoque 
        ('e' para entrada, 's' para saída).
    """
    funcionario = models.ForeignKey(User, on_delete=models.CASCADE)
    nf = models.PositiveIntegerField('Nota Fiscal', null=True, blank=True)
    movimento = models.CharField(max_length=1, choices=MOVIMENTO)

    class Meta:
        """
        Metadados para o modelo Estoque.

        Attributes:
            ordering (tuple): Define a ordenação padrão das 
            instâncias de Estoque. No caso, por 'criado_em' 
            em ordem decrescente.
        """
        ordering = ('-criado_em',)

    def __str__(self):
        """
        Retorna a representação em string do registro de estoque.

        Returns:
            str: O ID do registro de estoque.
        """
        return f'{self.pk}'
    

class EstoqueItens(models.Model):
    """
    Modelo que representa os itens de um registro de movimento 
    de estoque.

    Attributes:
        estoque (ForeignKey): Referência para o registro de 
        movimento de estoque.
        produto (ForeignKey): Referência para o produto no estoque.
        quantidade (PositiveIntegerField): Quantidade de produto 
        movimentada.
        saldo (PositiveIntegerField): Saldo atual do produto após 
        a movimentação.
    """

    estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    saldo = models.PositiveIntegerField()

    class Meta:
        """
        Metadados para o modelo EstoqueItens.

        Attributes:
            ordering (tuple): Define a ordenação padrão das instâncias
            de EstoqueItens. No caso, por 'pk' em ordem crescente.
        """
        ordering = ('pk',)

    def __str__(self):
        """
        Retorna a representação em string do item de estoque.

        Returns:
            str: A descrição do item de estoque incluindo seus IDs.
        """
        return f'{self.pk} - {self.estoque.pk} - {self.produto}'