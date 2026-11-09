from django.shortcuts import render, redirect ,get_object_or_404
from .models import Carrito, ItemCarrito, Pedido
from django.contrib.auth.decorators import login_required
from catalogo.models import Libro
from django.contrib import messages

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
        carrito = request.user.perfil.carrito,
    )

@login_required
def ver_carrito(request):
    carrito = _carrito_del_usuario(request)
    return render(request, 'carrito/ver_carrito.html',
                  {'items': carrito.itemcarrito_set.select_related('libro'),
                   'total': carrito.total(),
                   })

@login_required
def agregar_al_carrito(request, libro_id):
    #busca el libro en la bd utilizando su id
    libro = get_object_or_404(Libro, id=libro_id)
    #no hay unidades disponibles
    if libro.stock <= 0:
        messages.warning(request, f'{libro.titulo} no tiene stock')
        return redirect('lista_card')
    #obtiene el carrito del usuario
    carrito = _carrito_del_usuario(request)
    #retornar dos valores ibj item y creado devuelve booleano
    item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, libro=libro)
    #si el item ya estaba en el carrito sumamos 1 en el stock
    if not creado:
        if item.cantidad < libro.stock:
            item.cantidad += 1
            item.save()
        else:
            messages.warning(request, f'solo hay {libro.stock} unidades de {libro.titulo}')
    return redirect('ver_carrito')

@login_required
def incrementar_item(request, item_id):
    #busca el producto dentro del carrito del usuario actual
    item = _item_del_usuario(request, item_id)
    #comprobar que la cantidad actual sea menor al stock disponible
    if item.cantidad < item.libro.stock:
        item.cantidad += 1
        item.save()
    return redirect('ver_carrito')

@login_required
def disminuir_item(request, item_id):
    #busca el producto dentro del carrito del usuario actual
    item = _item_del_usuario(request, item_id)
    #comprobar que la cantidad actual sea mayor a 1
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    return redirect('ver_carrito')

@login_required
def eliminar_item(request, item_id):
    #busca el producto dentro del carrito del usuario actual
    item = _item_del_usuario(request, item_id)
    #eliminar el registro
    item.delete()
    return redirect('ver_carrito')