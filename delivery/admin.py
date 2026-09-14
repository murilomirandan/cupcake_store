from django.contrib import admin
from .models import Entrega


@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'status', 'codigoRastreio', 'atualizado_em')
    list_filter = ('status',)
    search_fields = ('pedido__numeroPedido', 'codigoRastreio')
    actions = ['marcar_a_caminho', 'marcar_entregue']

    def marcar_a_caminho(self, request, queryset):
        for entrega in queryset:
            entrega.atualizarStatus('A_CAMINHO')
    marcar_a_caminho.short_description = '🚚 Marcar como A caminho'

    def marcar_entregue(self, request, queryset):
        for entrega in queryset:
            entrega.atualizarStatus('ENTREGUE')
    marcar_entregue.short_description = '✅ Marcar como Entregue'