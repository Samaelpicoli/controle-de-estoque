from django.db import models

# Create your models here.

class Produto(models.Model):

    """
    Representa um produto no sistema de estoque.

    Attributes:
        importado (bool): Indica se o produto é importado.
        ncm (str): Nomenclatura Comum do Mercosul, usado para 
        classificação fiscal.
        produto (str): Nome do produto, deve ser único.
        preco (Decimal): Preço do produto com até 5 dígitos antes do
        ponto decimal e 2 dígitos após o ponto decimal.
        estoque (int): Quantidade de unidades disponíveis em estoque.
        estoque_minimo (int): Quantidade mínima recomendada em estoque.
    """
    importado = models.BooleanField(default=False)
    ncm = models.CharField('NCM', max_length=8)
    produto = models.CharField(max_length=100, unique=True)
    preco = models.DecimalField('preco', max_digits=7, decimal_places=2)
    estoque = models.IntegerField('estoque')
    estoque_minimo = models.PositiveIntegerField('estoque min', default=0)

    class Meta:
        """
        Metadados para o modelo Produto.

        Attributes:
            ordering (tuple): Define a ordenação padrão das instâncias
            de Produto. No caso, os produtos serão ordenados pelo 
            campo 'produto' em ordem crescente.

        """
        ordering = ('produto',)

    def __str__(self):
        """
        Retorna a representação em string do produto.

        Returns:
            str: O nome do produto.
        """
        return f'{self.produto}'