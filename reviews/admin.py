from django.contrib import admin
from .models import Avaliacao


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'pedido', 'nota', 'dataAvaliacao')
    list_filter = ('nota', 'dataAvaliacao')
    search_fields = ('cliente__email', 'pedido__numeroPedido', 'comentario')