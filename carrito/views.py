from django.shortcuts import render, redirect ,get_object_or_404
from .models import Carrito, ItemCarrito, Pedido
from django.contrib.auth.decorators import login_required

# Create your views here.
def _carrito_del_usuario(request):
    """Devuelve el carrito del usuario, si no existe lo crea"""
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user.perfil)
    return carrito
def _item_del_usuario(request, item_id):
    """Buscar un item solo dentro del carrito actual"""
    return get_object_or_404(
        ItemCarrito,
        id=item_id,
        carrito_del_usuario = request.user.perfil,
    )

@login_required
def ver_carrito(request):
    carrito = _carrito_del_usuario(request)
    return render(request, 'carrito/ver_carrito.html',
                  {'items': carrito.itemcarrito_set.select_related('libro'),
                   'total': carrito.total(),
                   })