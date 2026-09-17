from django.contrib import admin
from .models import Pedido, ItemPedido, StatusPedido


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ('subtotal',)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('numeroPedido', 'cliente', 'status', 'total', 'dataPedido')
    list_filter = ('status', 'dataPedido')
    search_fields = ('numeroPedido', 'cliente__email', 'cliente__nome')
    readonly_fields = ('numeroPedido', 'dataPedido', 'total')
    inlines = [ItemPedidoInline]

    actions = [
        'marcar_pago',
        'marcar_preparando',
        'marcar_saiu_entrega',
        'marcar_entregue',
        'marcar_cancelado',
    ]

    @admin.action(description='✅ Marcar como Pago')
    def marcar_pago(self, request, queryset):
        for pedido in queryset:
            pedido.alterarStatus(StatusPedido.PAGO)

    @admin.action(description='👨‍🍳 Marcar como Preparando')
    def marcar_preparando(self, request, queryset):
        for pedido in queryset:
            pedido.alterarStatus(StatusPedido.PREPARANDO)

    @admin.action(description='🚚 Marcar como Saiu para Entrega')
    def marcar_saiu_entrega(self, request, queryset):
        for pedido in queryset:
            pedido.alterarStatus(StatusPedido.SAIU_PARA_ENTREGA)

    @admin.action(description='✅ Marcar como Entregue')
    def marcar_entregue(self, request, queryset):
        for pedido in queryset:
            pedido.alterarStatus(StatusPedido.ENTREGUE)

    @admin.action(description='❌ Cancelar pedido')
    def marcar_cancelado(self, request, queryset):
        for pedido in queryset:
            pedido.alterarStatus(StatusPedido.CANCELADO)