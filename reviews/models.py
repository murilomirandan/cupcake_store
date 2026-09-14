import uuid
from django.db import models
from django.conf import settings
from orders.models import Pedido


class Avaliacao(models.Model):
    """US19 - Avaliar experiência"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='avaliacoes'
    )
    pedido = models.OneToOneField(
        Pedido, on_delete=models.CASCADE, related_name='avaliacao',
        null=True, blank=True
    )
    nota = models.PositiveSmallIntegerField()
    comentario = models.TextField(blank=True)
    dataAvaliacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-dataAvaliacao']
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'

    def __str__(self):
        return f'{self.cliente.nome} — {self.nota}⭐'

    def validarNota(self):
        return 1 <= self.nota <= 5

    def save(self, *args, **kwargs):
        if not self.validarNota():
            raise ValueError('A nota deve estar entre 1 e 5.')
        super().save(*args, **kwargs)