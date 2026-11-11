import time
from django.conf import settings # configuración del proyecto
from django.core.exceptions import ImproperlyConfigured # error de configuracion
from django.db import transaction # agrupa cambios en la base de datos
from django.db.models import F # resta de stock en la base de datos
from django.urls import reverse # construye URLs por nombre
from transbank.common.integration_type import IntegrationType # TEST o LIVE
from transbank.common.options import WebpayOptions # credenciales y ambiente
from transbank.webpay.webpay_plus.transaction import Transaction # transacciones
from django.shortcuts import render, redirect ,get_object_or_404
from .models import Carrito, ItemCarrito, Pedido
from django.contrib.auth.decorators import login_required
from catalogo.models import Libro
from django.contrib import messages


def _webpay_transaction():
    # Si falta alguna credencial, avisamos antes de llamar a Webpay
    if not settings.WEBPAY_COMMERCE_CODE or not settings.WEBPAY_API_KEY:
        raise ImproperlyConfigured("Faltan WEBPAY_COMMERCE_CODE o WEBPAY_API_KEY en el .env")
    # Elegimos el ambiente según la variable del .env
    ambiente = IntegrationType.LIVE if settings.WEBPAY_ENV == 'LIVE' else IntegrationType.TEST
    # Agrupamos las credenciales y el ambiente en un solo objeto
    options = WebpayOptions(
        commerce_code=settings.WEBPAY_COMMERCE_CODE, # código de comercio
        api_key=settings.WEBPAY_API_KEY, # clave de API
        integration_type=ambiente, # sandbox o real
    )
# Devolvemos el objeto que crea y confirma transacciones
    return Transaction(options)

# ---------- API ----------
@login_required
def iniciar_pago(request):
    # 1) Perfil del usuario y su carrito
    perfil = request.user.perfil
    carrito = get_object_or_404(Carrito, usuario=perfil)
    # 2) Monto total a pagar (entero en pesos)
    total = carrito.total()
    if total <= 0:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('ver_carrito')
    # 3) Pedido pendiente: se crea antes de ir a Webpay. El carrito no se toca.
    pedido = Pedido.objects.create(usuario=perfil, total=total, estado='PEND')
    request.session['pedido_id'] = pedido.id
    # 4) Identificador de la orden; la hora evita repetir el mismo buy_order
    buy_order = f"orden-{perfil.id}-{carrito.id}-{int(time.time())}"
    # 5) Identificador de sesión que Webpay devuelve al terminar
    session_id = str(perfil.id)
    # 6) URL absoluta a la que Webpay redirige al terminar el pago
    return_url = request.build_absolute_uri(reverse('pago_exitoso'))
    try:
    # 7) Crea la transacción con las credenciales del .env
        tx = _webpay_transaction()
    # 8) Pide a Webpay el token y la URL del formulario de pago
        response = tx.create(
            buy_order=buy_order,
            session_id=session_id,
            amount=total,
            return_url=return_url,
        )
    # 9) Envía al cliente al formulario de Webpay con el token
        return redirect(f"{response['url']}?token_ws={response['token']}")
    except Exception as e:
    # Si Webpay no responde, el pedido queda cancelado y el carrito se mantiene
        Pedido.objects.filter(pk=pedido.id).update(estado='CANC')
        messages.error(request, f"Error al iniciar el pago: {e}")
        return redirect('ver_carrito')
    
# ---------- API ----------
@login_required
def pago_exitoso(request):
    # 1) Sacamos el pedido de la sesión. Si ya no está, la página se recargó
    # o el pago ya se procesó, así que no hacemos nada de nuevo.
    pedido_id = request.session.pop('pedido_id', None)
    if not pedido_id:
        messages.info(request, "Este pago ya fue procesado.")
        return redirect('ver_carrito')
    pedido = get_object_or_404(Pedido, pk=pedido_id, usuario=request.user.perfil)
    # 2) Si el cliente anula en Webpay, el pedido queda cancelado y el carrito se mantiene
    if request.GET.get('TBK_TOKEN'):
        Pedido.objects.filter(pk=pedido.id).update(estado='CANC')
        messages.warning(request, "Cancelaste el pago. Tu carrito sigue disponible.")
        return redirect('ver_carrito')
    # 3) Token que Webpay envía al volver a nuestro sitio
    token = request.GET.get('token_ws')
    if not token:
        Pedido.objects.filter(pk=pedido.id).update(estado='CANC')
        messages.error(request, "No se recibió el token de Webpay.")
        return redirect('ver_carrito')
        # 4) Confirmamos la transacción con Webpay (commit)
    try:
        tx = _webpay_transaction()
        response = tx.commit(token)
        status = response.get('status')
    except Exception as e:
        Pedido.objects.filter(pk=pedido.id).update(estado='CANC')
        messages.error(request, f"Error al confirmar el pago: {e}")
        return redirect('ver_carrito')
    # 5) Si no fue autorizado, el pedido queda cancelado y el carrito se mantiene
    if status != 'AUTHORIZED':
        Pedido.objects.filter(pk=pedido.id).update(estado='CANC')
        messages.warning(request, f"El pago no fue autorizado ({status}). Tu carrito sigue disponible.")
        return redirect('ver_carrito')
    # 6) Pago autorizado: confirmamos el pedido, descontamos stock y vaciamos el carrito
    perfil = request.user.perfil
    carrito = get_object_or_404(Carrito, usuario=perfil)
    with transaction.atomic():
        Pedido.objects.filter(pk=pedido.id).update(estado='CONF')
        for item in carrito.itemcarrito_set.select_related('libro'):
            Libro.objects.filter(pk=item.libro_id).update(
                stock=F('stock') - item.cantidad
            )
        carrito.itemcarrito_set.all().delete()
    messages.success(request, "Pago exitoso con Webpay.")
    # 7) Mostramos la página de confirmación con el pedido y la respuesta de Webpay
    return render(request, 'carrito/confirmar_pedido.html', {
        'pedido': pedido,
        'response': response,
})

# ---------- Pedidos ----------
@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user.perfil).order_by('-fecha')
    return render(request, 'carrito/pedidos.html', {'pedidos': pedidos})


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