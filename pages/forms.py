from django import forms


class ContactForm(forms.Form):
    """Formulario de contacto. No persiste en base de datos: se procesa y
    se confirma al usuario mediante el sistema de mensajes de Django."""

    name = forms.CharField(
        label='Nombre',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    subject = forms.CharField(
        label='Asunto',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    message = forms.CharField(
        label='Mensaje',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
    )

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 10:
            raise forms.ValidationError('El mensaje debe tener al menos 10 caracteres.')
        return message
