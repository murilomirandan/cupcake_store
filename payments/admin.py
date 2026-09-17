from django.contrib import admin
from .models import Pagamento, PagamentoCartao, PagamentoPIX


class PagamentoCartaoInline(admin.StackedInline):
    model = PagamentoCartao
    extra = 0
    can_delete = False
    verbose_name_plural = 'Detalhes do Cartão'
    fields = ('numeroCarta', 'nomeTitular', 'parcelas', 'bandeira')


class PagamentoPIXInline(admin.StackedInline):
    model = PagamentoPIX
    extra = 0
    can_delete = False
    verbose_name_plural = 'Detalhes do PIX'
    fields = ('codigoPix', 'dataExpiracao')
    readonly_fields = ('codigoPix', 'dataExpiracao')

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'forma_badge', 'status_badge', 'valor_fmt', 'criado_em')
    list_filter = ('forma', 'status')
    search_fields = ('pedido__numeroPedido',)
    date_hierarchy = 'criado_em'

    @admin.display(description='Forma')
    def forma_badge(self, obj):
        cores = {
            'CARTAO_CREDITO': '💳',
            'CARTAO_DEBITO': '💳',
            'PIX': '📱',
        }
        return f"{cores.get(obj.forma, '')} {obj.get_forma_display()}"

    @admin.display(description='Status')
    def status_badge(self, obj):
        cores = {
            'AGUARDANDO': '🟡',
            'APROVADO': '🟢',
            'RECUSADO': '🔴',
            'ESTORNADO': '⚪',
        }
        return f"{cores.get(obj.status, '')} {obj.get_status_display()}"

    @admin.display(description='Valor')
    def valor_fmt(self, obj):
        return f'R$ {obj.valor}'