from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.vitrine_view, name='vitrine'),
    path('cupcake/<uuid:slug_id>/', views.detalhe_view, name='detalhe'),
]