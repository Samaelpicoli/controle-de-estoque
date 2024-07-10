from django.db import models

from django.urls import reverse_lazy

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
        categoria (ForeignKey): Referência à categoria do produto. Pode 
        ser nulo, se a categoria for removida, o campo é definido como 
        null.
    """
    importado = models.BooleanField(default=False)
    ncm = models.CharField('NCM', max_length=8)
    produto = models.CharField(max_length=100, unique=True)
    preco = models.DecimalField('preco', max_digits=7, decimal_places=2)
    estoque = models.IntegerField('estoque')
    estoque_minimo = models.PositiveIntegerField('estoque min', default=0)
    categoria = models.ForeignKey(
        'Categoria', 
        on_delete=models.SET_NULL, 
        null=True
    )

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
    
    def get_absolute_url(self):
        """
        Retorna a URL absoluta para o detalhe de um produto específico.
        
        Returns:
            str: A URL para a visualização de detalhe do produto.
        """
        return reverse_lazy('produto:detalhe_produto', kwargs={'pk':self.pk})
    

    def dict_to_json(self):
        """
        Retorna um dicionário representando os dados do produto
        para conversão em JSON.

        Este método é utilizado para serializar os dados principais
        do produto em um formato de dicionário, adequado para 
        conversão em JSON, facilitando a integração com APIs ou 
        outras funcionalidades que requeiram dados em formato JSON.

        Returns:
            dict: Um dicionário contendo o identificador primário (pk), 
            o nome do produto, e a quantidade de estoque.
        """
        return {
            'pk': self.pk,
            'produto': self.produto,
            'estoque': self.estoque,
        }
    

class Categoria(models.Model):
    """
    Representa uma categoria de produtos.

    Attributes:
        categoria (str): O nome da categoria. Deve ser único e
        tem um tamanho máximo de 100 caracteres.

    Meta:
        ordering (tuple): Define a ordenação padrão para as instâncias
        do modelo pela categoria em ordem alfabética.
    """
    categoria = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('categoria',)

    def __str__(self):
        """
        Retorna a representação em string da instância do modelo.

        Returns:
            str: O nome da categoria.
        """
        return self.categoria