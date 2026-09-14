from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.listar_view, name='listar'),
    path('<uuid:notificacao_id>/lida/', views.marcar_lida_view, name='marcar_lida'),
]