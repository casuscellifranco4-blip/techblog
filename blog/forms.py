from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Formulario para crear/editar publicaciones, con validaciones propias."""

    class Meta:
        model = Post
        fields = ['title', 'category', 'summary', 'content', 'image', 'status']
        labels = {
            'title': 'Título',
            'category': 'Categoría',
            'summary': 'Resumen',
            'content': 'Contenido',
            'image': 'Imagen (opcional)',
            'status': 'Estado',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 5:
            raise forms.ValidationError('El título debe tener al menos 5 caracteres.')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if len(content) < 20:
            raise forms.ValidationError('El contenido debe tener al menos 20 caracteres.')
        return content


class CommentForm(forms.ModelForm):
    """Formulario para comentar una publicación."""

    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': ''}
        widgets = {
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escribí tu comentario...'}
            ),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if len(content) < 2:
            raise forms.ValidationError('El comentario no puede estar vacío.')
        return content
