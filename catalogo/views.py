from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import ProtectedError
from .models import Libro, Categoria, Editorial, Autor
from .forms import LibroForm, CategoriaForm, EditorialForm, AutorForm


#LIBROS
def lista_libros(request):
    #obtener todos los libros de la bd
    libro = Libro.objects.all()
    return render(request, 'catalogo/libro/libro_list.html', {'libros': libro})

def crear_libros(request):
    #request.FILES es necesario para recibir la imagen de portada
    form = LibroForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            #si es valido se guarda el nuevo registro
            form.save()
            messages.success(request, 'Libro creado correctamente.')
            return redirect('lista_libros')
    #sino se renderiza al formulario del libro
    return render(request, 'catalogo/libro/libro_form.html', {'form': form, 'accion': 'Crear'})

def editar_libros(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    form = LibroForm(request.POST or None, request.FILES or None, instance=libro)
    if request.method == 'POST':
        if form.is_valid():
            #si es valido se actualiza el registro
            form.save()
            messages.success(request, 'Libro actualizado correctamente.')
            return redirect('lista_libros')
    #sino se renderiza al formulario del libro
    return render(request, 'catalogo/libro/libro_form.html', {'form': form, 'accion': 'Editar'})

def eliminar_libros(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        #se elimina el libro
        libro.delete()
        messages.success(request, 'Libro eliminado correctamente.')
        return redirect('lista_libros')
    #sino se renderiza a eliminar libro
    return render(request, 'catalogo/libro/libro_delete.html', {'obj': libro})

def detalle_libros(request, pk):
    #obtener el libro por su id, si no existe muestra error 404
    libro = get_object_or_404(Libro, pk=pk)
    return render(request, 'catalogo/libro/libro_detail.html', {'obj': libro})

#CATEGORIAS
def lista_categorias(request):
    #obtener todas las categorias de la bd
    categoria = Categoria.objects.all()
    return render(request, 'catalogo/categoria/categoria_list.html', {'categorias': categoria})

def crear_categorias(request):
    form = CategoriaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            #si es valido se guarda el nuevo registro
            form.save()
            messages.success(request, 'Categoría creada correctamente.')
            return redirect('lista_categorias')
    #sino se renderiza al formulario de la categoria
    return render(request, 'catalogo/categoria/categoria_form.html', {'form': form, 'accion': 'Crear'})

def editar_categorias(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if request.method == 'POST':
        if form.is_valid():
            #si es valido se actualiza el registro
            form.save()
            messages.success(request, 'Categoría actualizada correctamente.')
            return redirect('lista_categorias')
    #sino se renderiza al formulario de la categoria
    return render(request, 'catalogo/categoria/categoria_form.html', {'form': form, 'accion': 'Editar'})

def eliminar_categorias(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        try:
            #se intenta eliminar la categoria
            categoria.delete()
            messages.success(request, 'Categoría eliminada correctamente.')
        except ProtectedError:
            #no se puede eliminar porque tiene libros asociados (PROTECT)
            messages.error(request, 'No se puede eliminar la categoría porque tiene libros asociados.')
        return redirect('lista_categorias')
    #sino se renderiza a eliminar categoria
    return render(request, 'catalogo/categoria/categoria_delete.html', {'obj': categoria})


#EDITORIALES
def lista_editoriales(request):
    #obtener todas las editoriales de la bd
    editorial = Editorial.objects.all()
    return render(request, 'catalogo/editorial/editorial_list.html', {'editoriales': editorial})

def crear_editoriales(request):
    form = EditorialForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            #si es valido se guarda el nuevo registro
            form.save()
            messages.success(request, 'Editorial creada correctamente.')
            return redirect('lista_editoriales')
    #sino se renderiza al formulario de la editorial
    return render(request, 'catalogo/editorial/editorial_form.html', {'form': form, 'accion': 'Crear'})

def editar_editoriales(request, pk):
    editorial = get_object_or_404(Editorial, pk=pk)
    form = EditorialForm(request.POST or None, instance=editorial)
    if request.method == 'POST':
        if form.is_valid():
            #si es valido se actualiza el registro
            form.save()
            messages.success(request, 'Editorial actualizada correctamente.')
            return redirect('lista_editoriales')
    #sino se renderiza al formulario de la editorial
    return render(request, 'catalogo/editorial/editorial_form.html', {'form': form, 'accion': 'Editar'})

def eliminar_editoriales(request, pk):
    editorial = get_object_or_404(Editorial, pk=pk)
    if request.method == 'POST':
        try:
            #se intenta eliminar la editorial
            editorial.delete()
            messages.success(request, 'Editorial eliminada correctamente.')
        except ProtectedError:
            #no se puede eliminar porque tiene libros asociados (PROTECT)
            messages.error(request, 'No se puede eliminar la editorial porque tiene libros asociados.')
        return redirect('lista_editoriales')
    #sino se renderiza a eliminar editorial
    return render(request, 'catalogo/editorial/editorial_delete.html', {'obj': editorial})

#AUTORES
def lista_autores(request):
    #obtener todos los autores de la bd
    autor = Autor.objects.all()
    return render(request, 'catalogo/autor/autor_list.html', {'autores': autor})

def crear_autores(request):
    form = AutorForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            #si es valido se guarda el nuevo registro
            form.save()
            messages.success(request, 'Autor creado correctamente.')
            return redirect('lista_autores')
    #sino se renderiza al formulario del autor
    return render(request, 'catalogo/autor/autor_form.html', {'form': form, 'accion': 'Crear'})

def editar_autores(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    form = AutorForm(request.POST or None, instance=autor)
    if request.method == 'POST':
        if form.is_valid():
            #si es valido se actualiza el registro
            form.save()
            messages.success(request, 'Autor actualizado correctamente.')
            return redirect('lista_autores')
    #sino se renderiza al formulario del autor
    return render(request, 'catalogo/autor/autor_form.html', {'form': form, 'accion': 'Editar'})

def eliminar_autores(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == 'POST':
        try:
            #se intenta eliminar el autor
            autor.delete()
            messages.success(request, 'Autor eliminado correctamente.')
        except ProtectedError:
            #no se puede eliminar porque tiene libros asociados (PROTECT)
            messages.error(request, 'No se puede eliminar el autor porque tiene libros asociados.')
        return redirect('lista_autores')
    #sino se renderiza a eliminar autor
    return render(request, 'catalogo/autor/autor_delete.html', {'obj': autor})