from .cart import get_cart


def cart(request):
    try:
        return {'carrinho': get_cart(request)}
    except Exception:
        return {'carrinho': None}