import uuid
from django.db import models
from django.conf import settings


class StatusPedido(models.TextChoices):
    PENDENTE = 'PENDENTE', 'Pendente'
    PAGO = 'PAGO', 'Pago'
    PREPARANDO = 'PREPARANDO', 'Preparando'
    SAIU_PARA_ENTREGA = 'SAIU_PARA_ENTREGA', 'Saiu para entrega'
    ENTREGUE = 'ENTREGUE', 'Entregue'
    CANCELADO = 'CANCELADO', 'Cancelado'


class Pedido(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numeroPedido = models.CharField(max_length=20, unique=True, editable=False)
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='pedidos')
    dataPedido = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=StatusPedido.choices, default=StatusPedido.PENDENTE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-dataPedido']

    def save(self, *args, **kwargs):
        if not self.numeroPedido:
            import random
            self.numeroPedido = f'PED{random.randint(100000, 999999)}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.numeroPedido


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    cupcake = models.ForeignKey('catalog.Cupcake', on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    precoUnitario = models.DecimalField(max_digits=8, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    

def alterarStatus(self, novo_status):
    self.status = novo_status
    self.save()
    from notifications.services import notificar_atualizacao_status
    notificar_atualizacao_status(self)