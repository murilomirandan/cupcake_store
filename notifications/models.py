import uuid
from django.db import models
from django.conf import settings


class TipoNotificacao(models.TextChoices):
    CONFIRMACAO_PEDIDO = 'CONFIRMACAO_PEDIDO', 'Confirmação de Pedido'
    ATUALIZACAO_STATUS = 'ATUALIZACAO_STATUS', 'Atualização de Status'
    PROMOCAO = 'PROMOCAO', 'Promoção'
    AVALIACAO = 'AVALIACAO', 'Avaliação'


class Notificacao(models.Model):
    """US18 - Receber confirmação do pedido"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='notificacoes'
    )
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    tipo = models.CharField(max_length=30, choices=TipoNotificacao.choices)
    lida = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'

    def __str__(self):
        return self.titulo

    def marcarComoLida(self):
        self.lida = True
        self.save()