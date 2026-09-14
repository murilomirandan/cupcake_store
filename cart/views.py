from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from catalog.models import Cupcake
from .cart import get_cart
from .models import ItemCarrinho


@require_POST
def adicionar_view(request, cupcake_id):
    carrinho = get_cart(request)
    cupcake = get_object_or_404(Cupcake, id=cupcake_id, ativo=True)
    quantidade = int(request.POST.get('quantidade', 1))
    carrinho.adicionarItem(cupcake, quantidade)
    messages.success(request, f'{cupcake.nome} adicionado ao carrinho!')
    return redirect('cart:visualizar')


def visualizar_view(request):
    carrinho = get_cart(request)
    return render(request, 'cart/carrinho.html', {
        'carrinho': carrinho,
        'itens': carrinho.itens.select_related('cupcake'),
    })


@require_POST
def remover_view(request, item_id):
    get_cart(request).removerItem(item_id)
    messages.info(request, 'Item removido.')
    return redirect('cart:visualizar')