from .models import Carrinho


def get_cart(request):
    if request.user.is_authenticated:
        carrinho, _ = Carrinho.objects.get_or_create(cliente=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        carrinho, _ = Carrinho.objects.get_or_create(
            session_key=request.session.session_key, cliente=None
        )
    return carrinho