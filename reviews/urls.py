from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('avaliar/<uuid:pedido_id>/', views.avaliar_view, name='avaliar'),
]