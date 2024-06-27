from django.db import models


class EstoqueEntradaManager(models.Manager):
    """
    Manager personalizado para o modelo de entrada de estoque.
    Este manager modifica o conjunto de consultas padrão para 
    filtrar apenas entradas de estoque.
    """
    def get_queryset(self):
        """
        Retorna o conjunto de consultas filtrado para 
        incluir apenas movimentos de entrada ('e').
        """
        return super(EstoqueEntradaManager, self).get_queryset().filter(
            movimento='e'
        )
    

class EstoqueSaidaManager(models.Manager):
    """
    Manager personalizado para o modelo de saída de estoque.
    Este manager modifica o conjunto de consultas padrão para 
    filtrar apenas saídas de estoque.
    """
    def get_queryset(self):
        """
        Retorna o conjunto de consultas filtrado para 
        incluir apenas movimentos de saída ('s').
        """
        return super(EstoqueSaidaManager, self).get_queryset().filter(
            movimento='s'
        )