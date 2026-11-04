from django.db import models
from django.contrib.auth.models import User

def rol_cliente_default():
    rol, _ = Rol.objects.get_or_create(nombre = 'Cliente')
    return rol.id

# Create your models here.
class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre
    
class Perfil(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.RESTRICT, default=rol_cliente_default)
    # El campo user cada usuario tiene un solo perfil
    # cada perfil pertenece a un solo usuario
    user = models.OneToOneField(User, on_delete=models.CASCADE)#si se elimina usuario, se elimina su perfil
    def __str__(self):
        return f"{self.user.username} - {self.rol.nombre}"