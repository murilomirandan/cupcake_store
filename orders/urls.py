from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('meus-pedidos/', views.meus_pedidos_view, name='meus_pedidos'),
    path('pedido/<uuid:pedido_id>/', views.detalhe_pedido_view, name='detalhe'),
]