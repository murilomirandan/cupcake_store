import uuid
from django.db import models
from orders.models import Pedido


class StatusEntrega(models.TextChoices):
    AGUARDANDO_RETIRADA = 'AGUARDANDO_RETIRADA', 'Aguardando retirada'
    A_CAMINHO = 'A_CAMINHO', 'A caminho'
    ENTREGUE = 'ENTREGUE', 'Entregue'


class Entrega(models.Model):
    """US15 - Acompanhar status da entrega"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pedido = models.OneToOneField(
        Pedido, on_delete=models.CASCADE, related_name='entrega'
    )
    dataEnvio = models.DateTimeField(null=True, blank=True)
    previsaoEntrega = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=25, choices=StatusEntrega.choices,
        default=StatusEntrega.AGUARDANDO_RETIRADA
    )
    codigoRastreio = models.CharField(max_length=50, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'

    def __str__(self):
        return f'Entrega {self.pedido.numeroPedido} — {self.get_status_display()}'

    def atualizarStatus(self, novo_status):
        """US24/15 - Atualiza status e reflete no pedido"""
        from orders.models import StatusPedido
        self.status = novo_status
        self.save()

        if novo_status == StatusEntrega.A_CAMINHO:
            self.pedido.alterarStatus(StatusPedido.SAIU_PARA_ENTREGA)
        elif novo_status == StatusEntrega.ENTREGUE:
            self.pedido.alterarStatus(StatusPedido.ENTREGUE)