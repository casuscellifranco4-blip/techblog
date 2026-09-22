from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm, ProfileForm


def register(request):
    """Registro de un usuario nuevo. Si ya está logueado, lo manda al inicio."""
    if request.user.is_authenticated:
        return redirect('pages:home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}! Tu cuenta fue creada correctamente.')
            return redirect('pages:home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    """Muestra el perfil del usuario autenticado."""
    return render(request, 'accounts/profile.html', {'profile': request.user.profile})


@login_required
def profile_edit(request):
    """Permite editar el perfil del usuario autenticado."""
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil fue actualizado correctamente.')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/profile_form.html', {'form': form})
