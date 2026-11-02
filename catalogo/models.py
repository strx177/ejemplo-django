from django.db import models
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=120, verbose_name='Nombre', unique=True)
    descripcion = models.TextField(verbose_name='Descripción', blank=True)
    def __str__(self):
        return self.nombre

class Editorial(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    sitio_web = models.URLField(verbose_name='Sitio Web', blank=True)
    pais = models.CharField(max_length=80, verbose_name='Pais', blank=True)
    def __str__(self):
        return self.nombre

class Autor(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, verbose_name='Apellido')
    nacionalidad = models.CharField(max_length=80, verbose_name='Nacionalidad', blank=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    
class Libro(models.Model):
    isbn = models.CharField(max_length=20, verbose_name='Isbn', unique=True)
    titulo = models.CharField(max_length=200, verbose_name='Título')
    descripcion = models.TextField(verbose_name='Descripción')
    anio_publicacion = models.PositiveIntegerField(verbose_name='Año de Publicacion')
    #imagen de portada opcional
    portada = models.ImageField(verbose_name='Portada', blank=True, null=True, upload_to='portadas')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    #un libro puede pertenecer a varias categorias; una categoria puede contener varios libros
    categoria = models.ManyToManyField(Categoria, related_name='libros', verbose_name='Categorias')
    #relacion uno a muchos cada libro pertenece a una sola categoria
    #PROTECT no permite eliminar la editorial si tiene libros asociados
    editorial = models.ForeignKey(Editorial, on_delete=models.PROTECT, related_name='libros')
    #relacion uno a muchos cada libro pertenece a un solo autor
    autor = models.ForeignKey(Autor, on_delete=models.PROTECT, related_name='libros')
    
    def __str__(self):
        return self.titulo