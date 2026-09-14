from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notificacao


@login_required
def listar_view(request):
    notificacoes = request.user.notificacoes.all()
    return render(request, 'notifications/listar.html', {
        'notificacoes': notificacoes
    })


@login_required
def marcar_lida_view(request, notificacao_id):
    notificacao = get_object_or_404(
        Notificacao, id=notificacao_id, cliente=request.user
    )
    notificacao.marcarComoLida()
    return redirect('notifications:listar')