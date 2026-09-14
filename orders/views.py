from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.cart import get_cart
from .models import Pedido
from .services import criar_pedido


@login_required
def checkout_view(request):
    carrinho = get_cart(request)
    if not carrinho.itens.exists():
        messages.warning(request, 'Seu carrinho está vazio.')
        return redirect('catalog:vitrine')

    if request.method == 'POST':
        pedido = criar_pedido(request.user, carrinho)
        messages.success(request, f'Pedido {pedido.numeroPedido} criado! Escolha o pagamento.')
        return redirect('payments:escolher', pedido_id=pedido.id)

    return render(request, 'orders/checkout.html', {'carrinho': carrinho})


@login_required
def meus_pedidos_view(request):
    return render(request, 'orders/meus_pedidos.html', {
        'pedidos': request.user.pedidos.all()
    })


@login_required
def detalhe_pedido_view(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)
    return render(request, 'orders/detalhe_pedido.html', {'pedido': pedido})