from django import forms
from .models import Libro, Categoria, Editorial, Autor

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = '__all__'
        
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class EditorialForm(forms.ModelForm):
    class Meta:
        model = Editorial
        fields = '__all__'
        
class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = '__all__'