from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Cupcake, Categoria


def vitrine_view(request):
    cupcakes = Cupcake.objects.filter(ativo=True)
    categoria_id = request.GET.get('categoria') or ''
    busca = request.GET.get('q') or ''

    if categoria_id:
        cupcakes = cupcakes.filter(categorias__id=categoria_id)

    if busca:
        cupcakes = cupcakes.filter(
            Q(nome__icontains=busca) | Q(sabor__icontains=busca)
        )

    destaques = Cupcake.objects.filter(ativo=True, destaque=True)[:6]

    paginator = Paginator(cupcakes, 12)
    page = request.GET.get('page')
    cupcakes_page = paginator.get_page(page)

    # Marca qual categoria está selecionada
    categorias = Categoria.objects.all()
    for cat in categorias:
        cat.selecionada = (str(cat.id) == categoria_id)

    return render(request, 'catalog/vitrine.html', {
        'cupcakes': cupcakes_page,
        'destaques': destaques,
        'categorias': categorias,
        'categoria_selecionada': categoria_id,
        'busca': busca,
    })

def detalhe_view(request, slug_id):
    cupcake = get_object_or_404(Cupcake, id=slug_id, ativo=True)
    return render(request, 'catalog/detalhe.html', {
        'cupcake': cupcake,
        'ingredientes': cupcake.ingredientes.all(),
        'alergenicos': cupcake.ingredientes.filter(alergenico=True),
    })