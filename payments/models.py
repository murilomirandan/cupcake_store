import uuid
from django.db import models
from orders.models import Pedido


class FormaPagamento(models.TextChoices):
    CARTAO_CREDITO = 'CARTAO_CREDITO', 'Cartão de Crédito'
    CARTAO_DEBITO = 'CARTAO_DEBITO', 'Cartão de Débito'
    PIX = 'PIX', 'PIX'


class StatusPagamento(models.TextChoices):
    AGUARDANDO = 'AGUARDANDO', 'Aguardando'
    APROVADO = 'APROVADO', 'Aprovado'
    RECUSADO = 'RECUSADO', 'Recusado'
    ESTORNADO = 'ESTORNADO', 'Estornado'


class Pagamento(models.Model):
    """US10 - Escolher forma de pagamento"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pedido = models.OneToOneField(
        Pedido, on_delete=models.CASCADE, related_name='pagamento'
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    forma = models.CharField(max_length=20, choices=FormaPagamento.choices)
    status = models.CharField(
        max_length=20, choices=StatusPagamento.choices,
        default=StatusPagamento.AGUARDANDO
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-criado_em']

    def __str__(self):
        return f'Pagamento {self.pedido.numeroPedido} — {self.get_forma_display()}'

    def processar(self):
        from .gateways import processar_pagamento
        return processar_pagamento(self)

    def estornar(self):
        self.status = StatusPagamento.ESTORNADO
        self.save()


class PagamentoCartao(Pagamento):
    """US11 - Pagar com cartão"""
    numeroCarta = models.CharField(max_length=19)  # mascarado
    nomeTitular = models.CharField(max_length=150)
    parcelas = models.PositiveIntegerField(default=1)
    bandeira = models.CharField(max_length=30, blank=True)

    def validarDadosCartao(self):
        import re
        nums = re.sub(r'\D', '', self.numeroCarta)
        return 13 <= len(nums) <= 19


class PagamentoPIX(Pagamento):
    """US12 - Pagar com PIX"""
    qrCode = models.TextField(blank=True)     # base64 da imagem
    codigoPix = models.CharField(max_length=255, blank=True)
    dataExpiracao = models.DateTimeField(null=True, blank=True)

    def gerarQRCode(self):
        import qrcode
        import base64
        from io import BytesIO
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(self.codigoPix or f'PIX-{self.pedido.numeroPedido}')
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        self.qrCode = base64.b64encode(buffer.getvalue()).decode()
        self.save()
        return self.qrCode