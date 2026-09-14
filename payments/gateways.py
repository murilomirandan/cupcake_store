"""Gateway de pagamento simulado para desenvolvimento"""
import uuid
from datetime import timedelta
from django.utils import timezone
from django.conf import settings


def processar_pagamento(pagamento):
    """
    Em produção: chamar API do Mercado Pago / Stripe / PagSeguro.
    Aqui simulamos a resposta.
    """
    from .models import StatusPagamento, PagamentoCartao, PagamentoPIX

    if isinstance(pagamento, PagamentoCartao):
        if not pagamento.validarDadosCartao():
            pagamento.status = StatusPagamento.RECUSADO
            pagamento.save()
            return False
        pagamento.status = StatusPagamento.APROVADO
        pagamento.save()
        return True

    if isinstance(pagamento, PagamentoPIX):
        pagamento.codigoPix = f'00020126580014BR.GOV.BCB.PIX{uuid.uuid4().hex[:20]}'
        pagamento.dataExpiracao = timezone.now() + timedelta(
            minutes=getattr(settings, 'PIX_EXPIRATION_MINUTES', 15)
        )
        pagamento.gerarQRCode()
        pagamento.status = StatusPagamento.AGUARDANDO
        pagamento.save()
        return True

    return False


def confirmar_pagamento_pix(pagamento):
    """Confirma pagamento PIX (chamado por polling/webhook)"""
    from .models import StatusPagamento
    if pagamento.status == StatusPagamento.AGUARDANDO:
        pagamento.status = StatusPagamento.APROVADO
        pagamento.save()
        from orders.models import StatusPedido
        pagamento.pedido.alterarStatus(StatusPedido.PAGO)
        return True
    return False