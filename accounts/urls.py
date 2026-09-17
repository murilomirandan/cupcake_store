from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('enderecos/', views.enderecos_view, name='enderecos'), 
]