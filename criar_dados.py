import os

from random import choice, random, randint

import string

import django


# Configura o ambiente do Django para este script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projeto.settings")
django.setup()


from produto.models import Produto


class Utils:
    """
    Classe utilitária com métodos genéricos.
    """

    @staticmethod
    def gerar_digitos(max_lenght):
        """
        Gera uma sequência de dígitos aleatórios.

        Args:
            max_lenght (int): O comprimento máximo da 
            sequência de dígitos.

        Returns:
            str: Uma string contendo dígitos aleatórios.
        """
        return str(''.join(choice(string.digits) for i in range(max_lenght)))
    

class ProdutoClass:

    """
    Classe responsável por operações relacionadas ao modelo Produto.
    """

    @staticmethod
    def criar_produtos(produtos):
        """
        Cria instâncias do modelo Produto no banco de dados.

        Args:
            produtos (tuple): Uma tupla contendo os nomes dos produtos
            a serem criados.
        """
        # Remove todos os registros existentes de Produto
        Produto.objects.all().delete()
        aux = []
        for produto in produtos:
            # Dados fictícios para criação de produtos
            dados = dict(
                produto = produto,
                importado=choice((True, False)),
                ncm = Utils.gerar_digitos(8),
                preco = random() * randint(10, 50),
                estoque = randint(10, 200)
            )

            # Cria uma instância de Produto com os dados fictícios
            objeto = Produto(**dados)
            aux.append(objeto)

        # Cria todos os produtos de uma vez no banco de dados
        Produto.objects.bulk_create(aux)


# Lista de nomes de produtos a serem criados
produtos = (
    'Apontador',
    'Caderno 100 folhas',
    'Caderno 200 folhas',
    'Caneta Azul',
    'Caneta Preta',
    'Caneta Vermelha',
    'Durex',
    'Giz',
    'Lapiseira 0.3mm',
    'Lápis de Cor',
    'Lápis',
    'Papel para impressora'
)


# Cria os produtos no banco de dados usando a classe ProdutoClass
ProdutoClass.criar_produtos(produtos)
