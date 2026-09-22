from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CommentForm, PostForm
from .models import Category, Post


class PostListView(ListView):
    """Listado público de publicaciones, con búsqueda y filtro por categoría."""

    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.filter(status='published').select_related('author', 'category')
        category_slug = self.request.GET.get('categoria')
        query = self.request.GET.get('q')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('categoria', '')
        context['query'] = self.request.GET.get('q', '')
        return context


class PostDetailView(DetailView):
    """Detalle de una publicación, con sus comentarios y el formulario para agregar uno."""

    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.select_related('author', 'category').prefetch_related('comments__author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(active=True)
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Crear una publicación nueva (requiere estar autenticado)."""

    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'La publicación fue creada correctamente.')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Editar una publicación existente (solo el autor puede hacerlo)."""

    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    login_url = 'login'

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'La publicación fue actualizada correctamente.')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Eliminar una publicación (solo el autor puede hacerlo)."""

    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    login_url = 'login'

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'La publicación fue eliminada.')
        return super().form_valid(form)


@login_required
def add_comment(request, slug):
    """Agrega un comentario a una publicación (requiere estar autenticado)."""
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Tu comentario fue publicado.')
        else:
            messages.error(request, 'No se pudo publicar el comentario. Revisá el formulario.')
    return redirect('blog:post_detail', slug=post.slug)
