from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    """Formulario de registro: además de usuario/clave, pide un email único."""

    email = forms.EmailField(required=True, label='Correo electrónico')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe una cuenta registrada con este correo electrónico.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class StyledAuthenticationForm(AuthenticationForm):
    """Formulario de login estándar de Django, pero con estilo Bootstrap."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class ProfileForm(forms.ModelForm):
    """Edición del perfil extendido del usuario."""

    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'website', 'location']
        labels = {
            'bio': 'Biografía',
            'avatar': 'Foto de perfil',
            'website': 'Sitio web',
            'location': 'Ubicación',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'maxlength': 500}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_bio(self):
        bio = self.cleaned_data.get('bio', '')
        if len(bio) > 500:
            raise forms.ValidationError('La biografía no puede superar los 500 caracteres.')
        return bio
