from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Pedido, StatusPedido
from .models import Avaliacao


@login_required
def avaliar_view(request, pedido_id):
    """US19 - Avaliar experiência"""
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)

    if pedido.status != StatusPedido.ENTREGUE:
        messages.warning(request, 'Você só pode avaliar pedidos entregues.')
        return redirect('orders:meus_pedidos')

    if hasattr(pedido, 'avaliacao'):
        messages.info(request, 'Você já avaliou este pedido.')
        return redirect('orders:meus_pedidos')

    if request.method == 'POST':
        nota = int(request.POST.get('nota', 0))
        comentario = request.POST.get('comentario', '').strip()
        if 1 <= nota <= 5:
            Avaliacao.objects.create(
                cliente=request.user, pedido=pedido,
                nota=nota, comentario=comentario
            )
            messages.success(request, 'Obrigado por avaliar! 💖')
            return redirect('orders:meus_pedidos')
        else:
            messages.error(request, 'Escolha uma nota de 1 a 5.')

    return render(request, 'reviews/avaliar.html', {'pedido': pedido})