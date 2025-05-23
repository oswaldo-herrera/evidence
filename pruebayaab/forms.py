from django import forms
from django.contrib.auth.models import User 
from .models import Categoria, Producto, Tarea, NodoOrganigrama

class Formularioyaab(forms.Form):

    nombre = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe tu nombre'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escribe tu email'})
    )
    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe tu mensaje', 'rows': 4})
    )
    telefonico = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe tu numero telefonico', 'type':'tel'})
    )

class FormularioRegistro(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password_confirmacion = forms.CharField(widget=forms.PasswordInput, label="Confirmación de Contraseña")

    class Meta:
        model = User  # O tu modelo personalizado
        fields = ('username', 'email', 'first_name',) # Campos a mostrar en el formulario
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Correo Electrónico',
            'first_name': 'Nombre',
            
        }
        help_texts = {
            'username': None,  # Elimina el texto de ayuda predeterminado
        }

    def clean_password_confirmacion(self):
        password = self.cleaned_data.get('password')
        password_confirmacion = self.cleaned_data.get('password_confirmacion')
        if password != password_confirmacion:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password_confirmacion

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password']
        user.set_password(password)
        if commit:
            user.save()
        return user

# >>>>>Ahora estoy usando clases para manejar la categoria en el CRUD<<<<<<
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion'] #Fecha esta generado automaticamente.
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }


#>>>>>>PRODUCTO
class ProductoForm(forms.ModelForm):
    #categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), empty_label="Selecciona una categoría", required=True)

   class Meta:
    model = Producto
    fields = ['nombre', 'descripcion', 'costo', 'stock', 'categoria', 'disponible']



class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'fecha_vencimiento']  # Excluimos 'usuario' y 'completada'

        widgets = {
            'fecha_vencimiento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


#organigrama>>>>
class NodoForm(forms.ModelForm):
    class Meta:
        model = NodoOrganigrama
        fields = ['nombre', 'puesto']