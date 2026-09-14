from django.contrib import admin
from .models import Pagamento, PagamentoCartao, PagamentoPIX


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'forma', 'status', 'valor', 'criado_em')
    list_filter = ('forma', 'status')
    search_fields = ('pedido__numeroPedido',)


admin.site.register(PagamentoCartao)
admin.site.register(PagamentoPIX)