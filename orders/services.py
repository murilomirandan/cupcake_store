from decimal import Decimal
from django.db import transaction
from .models import Pedido, ItemPedido, StatusPedido


@transaction.atomic
def criar_pedido(cliente, carrinho):
    pedido = Pedido.objects.create(cliente=cliente, total=carrinho.valorTotal)
    for item in carrinho.itens.all():
        ItemPedido.objects.create(
            pedido=pedido,
            cupcake=item.cupcake,
            quantidade=item.quantidade,
            precoUnitario=item.precoUnitario,
            subtotal=item.subtotal,
        )
    carrinho.itens.all().delete()
    carrinho.valorTotal = Decimal('0.00')
    carrinho.save()
    
    # Notifica o cliente (US18)
    from notifications.services import notificar_confirmacao_pedido
    notificar_confirmacao_pedido(pedido)
    
    return pedido