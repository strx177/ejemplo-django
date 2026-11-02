from django.contrib import admin
from .models import Libro, Categoria, Editorial, Autor

# Register your models here.
admin.site.register(Libro)
admin.site.register(Categoria)
admin.site.register(Editorial)
admin.site.register(Autor)