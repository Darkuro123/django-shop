from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class ClienteForm(forms.Form):
    SEXO_CHOICES = {
        ('M', 'Masculino'),
        ('F', 'Femenino')
    }
    dni = forms.CharField(label="DNI",max_length=8)
    nombre = forms.CharField(label="Nombres",max_length=200, required=True)
    apellido = forms.CharField(label="Apellidos",max_length=200, required=True)
    email = forms.EmailField(label="email",max_length=200, required=True)
    direccion = forms.CharField(label="direccion",widget=forms.Textarea)
    telefono = forms.CharField(max_length=20)
    sexo = forms.ChoiceField(label="sexo", choices=SEXO_CHOICES)
    fecha_nacimiento = forms.DateField(label="fecha nacimiento",input_formats=['%Y-%m-%d'],widget=DateInput())
    # contraseña = forms.CharField(label="Contraseña",max_length=200, required=True)

    