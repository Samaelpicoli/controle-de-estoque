from django.shortcuts import render

from .models import Produto

# Create your views here.

def lista_produtos(request):
    nome_template = 'lista_produtos.html'

    objetos = Produto.objects.all()
    
    contexto = {'lista_objetos': objetos}

    return render(request, template_name=nome_template, context=contexto)