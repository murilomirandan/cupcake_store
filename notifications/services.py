from .models import Notificacao, TipoNotificacao


def notificar_confirmacao_pedido(pedido):
    """US18 - Receber confirmação do pedido"""
    return Notificacao.objects.create(
        cliente=pedido.cliente,
        titulo=f'Pedido {pedido.numeroPedido} confirmado! 🎉',
        mensagem=(
            f'Seu pedido foi confirmado e está sendo preparado. '
            f'Total: R$ {pedido.total}.'
        ),
        tipo=TipoNotificacao.CONFIRMACAO_PEDIDO,
    )


def notificar_atualizacao_status(pedido):
    """US18 - Notificar mudança de status"""
    return Notificacao.objects.create(
        cliente=pedido.cliente,
        titulo='Status atualizado',
        mensagem=(
            f'Seu pedido {pedido.numeroPedido} agora está: '
            f'{pedido.get_status_display()}.'
        ),
        tipo=TipoNotificacao.ATUALIZACAO_STATUS,
    )