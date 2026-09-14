from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta

from orders.models import Pedido, StatusPedido
from .models import (
    PagamentoCartao, PagamentoPIX,
    FormaPagamento, StatusPagamento
)


@login_required
def escolher_forma_view(request, pedido_id):
    """US10 - Escolher forma de pagamento"""
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)

    # Se já tem pagamento aprovado, não deixa pagar de novo
    if hasattr(pedido, 'pagamento') and pedido.pagamento.status == StatusPagamento.APROVADO:
        messages.info(request, 'Este pedido já foi pago.')
        return redirect('orders:detalhe', pedido_id=pedido.id)

    if request.method == 'POST':
        forma = request.POST.get('forma')
        formas_validas = [f.value for f in FormaPagamento]

        if forma not in formas_validas:
            messages.error(request, 'Forma de pagamento inválida.')
            return redirect('payments:escolher', pedido_id=pedido.id)

        if forma == FormaPagamento.PIX:
            pagamento = PagamentoPIX.objects.create(
                pedido=pedido, valor=pedido.total, forma=forma
            )
            pagamento.processar()
            return redirect('payments:pix', pagamento_id=pagamento.id)
        else:
            return redirect('payments:cartao', pedido_id=pedido.id, forma=forma)

    return render(request, 'payments/escolher.html', {'pedido': pedido})


@login_required
def cartao_view(request, pedido_id):
    """US11 - Pagar com cartão"""
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)
    forma = request.GET.get('forma', FormaPagamento.CARTAO_CREDITO)

    if request.method == 'POST':
        numero = request.POST.get('numeroCarta', '').replace(' ', '')
        titular = request.POST.get('nomeTitular', '')
        parcelas = int(request.POST.get('parcelas', 1))

        if not numero or not titular:
            messages.error(request, 'Preencha todos os campos do cartão.')
            return redirect('payments:cartao', pedido_id=pedido.id)

        pagamento = PagamentoCartao.objects.create(
            pedido=pedido,
            valor=pedido.total,
            forma=forma,
            numeroCarta=f'**** **** **** {numero[-4:]}',
            nomeTitular=titular,
            parcelas=parcelas,
        )

        # Guardamos o número real temporariamente para validar (não persiste)
        pagamento.numeroCarta = numero
        sucesso = pagamento.processar()

        if sucesso:
            pedido.alterarStatus(StatusPedido.PAGO)
            messages.success(request, 'Pagamento aprovado! 🎉')
            return redirect('orders:detalhe', pedido_id=pedido.id)
        else:
            messages.error(request, 'Pagamento recusado. Verifique os dados.')
            return redirect('payments:cartao', pedido_id=pedido.id)

    return render(request, 'payments/cartao.html', {
        'pedido': pedido, 'forma': forma
    })


@login_required
def pix_view(request, pagamento_id):
    """US12 - Pagar com PIX"""
    pagamento = get_object_or_404(
        PagamentoPIX, id=pagamento_id, pedido__cliente=request.user
    )
    return render(request, 'payments/pix.html', {'pagamento': pagamento})


@login_required
def verificar_pix_view(request, pagamento_id):
    """Polling para verificar se o PIX foi pago"""
    pagamento = get_object_or_404(PagamentoPIX, id=pagamento_id)

    # Simulação: considera pago após 10 segundos
    if pagamento.status == StatusPagamento.AGUARDANDO:
        if timezone.now() > pagamento.criado_em + timedelta(seconds=10):
            from .gateways import confirmar_pagamento_pix
            confirmar_pagamento_pix(pagamento)
            pagamento.refresh_from_db()

    return JsonResponse({
        'status': pagamento.status,
        'aprovado': pagamento.status == StatusPagamento.APROVADO,
        'redirecionar': f'/pedidos/pedido/{pagamento.pedido.id}/',
    })