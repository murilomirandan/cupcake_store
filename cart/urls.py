from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.visualizar_view, name='visualizar'),
    path('adicionar/<uuid:cupcake_id>/', views.adicionar_view, name='adicionar'),
    path('remover/<uuid:item_id>/', views.remover_view, name='remover'),
    path('atualizar/<uuid:item_id>/', views.atualizar_view, name='atualizar'),
]