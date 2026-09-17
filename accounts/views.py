from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Endereco

from .forms import CadastroClienteForm, LoginForm, EnderecoForm

@login_required
def perfil_view(request):
    """Página 'Meu Perfil'"""
    return render(request, 'accounts/perfil.html', {'user_obj': request.user})

def enderecos_view(request):
    """US14 - Listar e cadastrar endereços"""
    enderecos = Endereco.objects.filter(cliente=request.user)

    if request.method == 'POST':
        form = EnderecoForm(request.POST)
        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.cliente = request.user
            if endereco.validarCEP():
                endereco.save()
                messages.success(request, 'Endereço cadastrado com sucesso!')
                return redirect('accounts:enderecos')
            else:
                messages.error(request, 'CEP inválido.')
        else:
            messages.error(request, 'Corrija os erros no formulário.')
    else:
        form = EnderecoForm()

    return render(request, 'accounts/enderecos.html', {
        'enderecos': enderecos,
        'form': form,
    })

def cadastro_view(request):
    """US16 - Criar conta"""
    if request.user.is_authenticated:
        return redirect('catalog:vitrine')

    if request.method == 'POST':
        form = CadastroClienteForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f'Bem-vindo(a), {user.nome}! Sua conta foi criada com sucesso. 🧁'
            )
            return redirect('catalog:vitrine')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = CadastroClienteForm()

    return render(request, 'accounts/cadastro.html', {'form': form})


def login_view(request):
    """US17 - Fazer login"""
    if request.user.is_authenticated:
        return redirect('catalog:vitrine')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bem-vindo(a) de volta, {user.nome}!')
            return redirect('catalog:vitrine')
        else:
            messages.error(request, 'E-mail ou senha incorretos.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('catalog:vitrine')