from django.db import models
from registro.models import Perfil
from catalogo.models import Libro

class Carrito(models.Model):
    usuario = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    creando = models.DateField(auto_now_add=True)
    #metodo para calcular el total del carrito
    def total(self):
        total = 0
        for item in self.itemcarrito_set.all():
            total += item.subtotal()
        return total 
    def __str__(self):
        return f'Carrito de {self.usuario.user.username}'
    
class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    #metodo para calcular el precio item
    def subtotal(self):
        return self.cantidad * self.libro.precio
    
    def __str__(self):
        return f'{self.cantidad} x {self.libro.titulo}'
    
class Pedido(models.Model):
    ESTADOS = [
        ('PEND', 'Pendiente'),
        ('CONF', 'Confirmado'),
        ('CANC', 'Cancelado'),
    ]
    usuario = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    decha = models.DateTimeField(auto_now_add=True)
    total = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=4, choices=ESTADOS, default='Pendiente')
    def __str__(self):
        return f'Pedido #{self.id} - {self.usuario.user.username}'