from django.contrib import messages
from django.shortcuts import redirect, render

from blog.models import Post

from .forms import ContactForm


def home(request):
    """Página de inicio: muestra las últimas publicaciones del blog."""
    latest_posts = Post.objects.filter(status='published').select_related('category')[:3]
    return render(request, 'pages/home.html', {'latest_posts': latest_posts})


def about(request):
    """Página estática 'Acerca de'."""
    return render(request, 'pages/about.html')


def contact(request):
    """Formulario de contacto con validación."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Gracias por tu mensaje. Te responderemos a la brevedad.')
            return redirect('pages:contact')
    else:
        form = ContactForm()

    return render(request, 'pages/contact.html', {'form': form})
