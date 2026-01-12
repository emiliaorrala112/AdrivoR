from .models import Producto
from django.db.models import F

def alertas_stock(request):
    if request.user.is_authenticated and request.user.is_staff:
        bajos = Producto.objects.filter(stock__lte=F('stock_minimo'))
    else:
        bajos = []
    return {'productos_bajo_stock': bajos}

def contador_carrito(request):
    total = 0
    # Verificamos si existe el carrito
    if 'carrito' in request.session:
        for key, value in request.session['carrito'].items():
            try:
                # INTENTO 1: Si es un diccionario (Formato correcto)
                if isinstance(value, dict) and 'cantidad' in value:
                    total += int(value['cantidad'])
                # INTENTO 2: Si es solo un número (Formato antiguo/error)
                elif isinstance(value, int):
                    total += value
            except Exception:
                # Si falla, no hacemos nada, solo ignoramos el error
                pass
                
    return {'cantidad_carrito': total}