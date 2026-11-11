from django.urls import path
from .import views

urlpatterns = [
    path('ver/', views.ver_carrito, name='ver_carrito'),
    path('agregar/<int:libro_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('mas/<int:item_id>/', views.incrementar_item, name='incrementar_item'),
    path('menos/<int:item_id>/', views.disminuir_item, name='disminuir_item'),
    path('eliminar/<int:item_id>/', views.eliminar_item, name='eliminar_item'),
    #pago
    path('pagar/', views.iniciar_pago, name='iniciar_pago'),
    path('pago-exitoso/', views.pago_exitoso, name='pago_exitoso'),
    #Pedidos
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos')
]