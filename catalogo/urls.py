from django.urls import path
from . import views

urlpatterns = [
    #libros
    path('', views.lista_libros, name='lista_libros'),
    path('crear/', views.crear_libros, name='crear_libros'),
    path('<int:pk>/editar/', views.editar_libros, name='editar_libros'),
    path('<int:pk>/eliminar/', views.eliminar_libros, name='eliminar_libros'),
    path('libros/<int:pk>/', views.detalle_libros, name='detalle_libros'),
    
    #categorias
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/crear/', views.crear_categorias, name='crear_categorias'),
    path('categorias/<int:pk>/editar/', views.editar_categorias, name='editar_categorias'),
    path('categorias/<int:pk>/eliminar/', views.eliminar_categorias, name='eliminar_categorias'),
    
    #editoriales
    path('editoriales/', views.lista_editoriales, name='lista_editoriales'),
    path('editoriales/crear/', views.crear_editoriales, name='crear_editoriales'),
    path('editoriales/<int:pk>/editar/', views.editar_editoriales, name='editar_editoriales'),
    path('editoriales/<int:pk>/eliminar/', views.eliminar_editoriales, name='eliminar_editoriales'),
    
    #autores
    path('autores/', views.lista_autores, name='lista_autores'),
    path('autores/crear/', views.crear_autores, name='crear_autores'),
    path('autores/<int:pk>/editar/', views.editar_autores, name='editar_autores'),
    path('autores/<int:pk>/eliminar/', views.eliminar_autores, name='eliminar_autores'),
]
    