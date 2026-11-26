from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Usuario


class FormularioDatosUsuario(forms.ModelForm):
    rol = forms.ModelChoiceField(
        queryset=Group.objects.none(),
        label='Rol',
        empty_label='Seleccioná un rol',
    )

    class Meta:
        model = Usuario
        fields = ('nombre', 'apellido', 'dni', 'telefono', 'email', 'fecha_nacimiento', 'is_active')
        widgets = {
            'nombre': forms.TextInput(attrs={
                'autofocus': True,
                'pattern': '[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+',
                'title': 'Ingresá solo letras y espacios.',
            }),
            'apellido': forms.TextInput(attrs={
                'pattern': '[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+',
                'title': 'Ingresá solo letras y espacios.',
            }),
            'dni': forms.TextInput(attrs={
                'inputmode': 'numeric', 'maxlength': 8, 'pattern': r'\d{7,8}',
                'title': 'El DNI debe tener 7 u 8 dígitos.',
            }),
            'telefono': forms.TextInput(attrs={
                'inputmode': 'tel', 'maxlength': 15, 'pattern': r'\d{8,15}',
                'title': 'El teléfono debe tener entre 8 y 15 dígitos, sin espacios.',
            }),
            'email': forms.EmailInput(),
            'fecha_nacimiento': forms.DateInput(format='%d/%m/%Y', attrs={
                'placeholder': 'dd/mm/aaaa', 'inputmode': 'numeric', 'maxlength': 10,
                'pattern': r'\d{2}/\d{2}/\d{4}',
                'title': 'Ingresá la fecha en formato día/mes/año (ejemplo: 15/01/2000).',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_nacimiento'].input_formats = ['%d/%m/%Y']
        self.fields['rol'].queryset = Group.objects.all().order_by('name')

        if self.instance and self.instance.pk:
            self.fields['rol'].initial = self.instance.groups.first()

    def _limpiar_nombre(self, campo):
        valor = ' '.join(self.cleaned_data[campo].split())
        if not valor.replace(' ', '').isalpha():
            raise ValidationError('Ingresá solo letras y espacios.')
        return valor

    def clean_nombre(self):
        return self._limpiar_nombre('nombre')

    def clean_apellido(self):
        return self._limpiar_nombre('apellido')

    def clean_dni(self):
        dni = self.cleaned_data['dni'].strip()
        if not dni.isdigit() or not 7 <= len(dni) <= 8:
            raise ValidationError('Ingresá un DNI válido de 7 u 8 dígitos.')
        return dni

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono'].strip()
        if not telefono.isdigit() or not 8 <= len(telefono) <= 15:
            raise ValidationError('Ingresá un teléfono de 8 a 15 dígitos, sin espacios.')
        return telefono

    def clean_email(self):
        return self.cleaned_data['email'].strip().lower()

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data['fecha_nacimiento']
        hoy = timezone.localdate()
        if fecha >= hoy:
            raise ValidationError('La fecha de nacimiento debe ser anterior a hoy.')
        if fecha.year < hoy.year - 120:
            raise ValidationError('Ingresá una fecha de nacimiento válida.')
        return fecha

    def guardar_rol(self, usuario):
        usuario.groups.set([self.cleaned_data['rol']])


class FormularioAltaUsuario(FormularioDatosUsuario):
    contrasena = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
        help_text='Debe cumplir las reglas de seguridad de Django.',
    )
    confirmar_contrasena = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput,
    )

    def clean_confirmar_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena')
        confirmar_contrasena = self.cleaned_data['confirmar_contrasena']
        if contrasena and contrasena != confirmar_contrasena:
            raise ValidationError('Las contraseñas no coinciden.')
        return confirmar_contrasena

    def clean_contrasena(self):
        contrasena = self.cleaned_data['contrasena']
        validate_password(contrasena, self.instance)
        return contrasena

    def save(self, commit=True):
        usuario = forms.ModelForm.save(self, commit=False)
        usuario.set_password(self.cleaned_data['contrasena'])
        if commit:
            usuario.save()
            self.guardar_rol(usuario)
        return usuario


class FormularioEdicionUsuario(FormularioDatosUsuario):
    def save(self, commit=True):
        usuario = super().save(commit=commit)
        if commit:
            self.guardar_rol(usuario)
        return usuario


class FormularioCambioAdministrador(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Usuario
        fields = '__all__'
