import uuid
from django.db import models
from django.conf import settings
from catalog.models import Cupcake


class Carrinho(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='carrinho', null=True, blank=True
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    valorTotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def adicionarItem(self, cupcake, quantidade=1):
        item, created = ItemCarrinho.objects.get_or_create(
            carrinho=self, cupcake=cupcake,
            defaults={'quantidade': quantidade, 'precoUnitario': cupcake.preco}
        )
        if not created:
            item.quantidade += quantidade
            item.save()
        self.calcularTotal()
        return item

    def removerItem(self, item_id):
        ItemCarrinho.objects.filter(id=item_id, carrinho=self).delete()
        self.calcularTotal()

    def calcularTotal(self):
        total = sum(item.subtotal for item in self.itens.all())
        self.valorTotal = total
        self.save()
        return total

    @property
    def quantidade_itens(self):
        return sum(i.quantidade for i in self.itens.all())


class ItemCarrinho(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name='itens')
    cupcake = models.ForeignKey(Cupcake, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    precoUnitario = models.DecimalField(max_digits=8, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('carrinho', 'cupcake')

    def save(self, *args, **kwargs):
        self.subtotal = self.precoUnitario * self.quantidade
        super().save(*args, **kwargs)