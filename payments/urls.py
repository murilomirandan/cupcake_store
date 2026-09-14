from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('escolher/<uuid:pedido_id>/', views.escolher_forma_view, name='escolher'),
    path('cartao/<uuid:pedido_id>/', views.cartao_view, name='cartao'),
    path('pix/<uuid:pagamento_id>/', views.pix_view, name='pix'),
    path('pix/<uuid:pagamento_id>/verificar/', views.verificar_pix_view, name='verificar_pix'),
]