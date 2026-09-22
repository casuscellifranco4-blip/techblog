from django.contrib import admin, messages

from .models import Category, Comment, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('author', 'created_at')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('content', 'author__username')
    actions = ['approve_comments', 'deactivate_comments']

    @admin.action(description='Aprobar comentarios seleccionados')
    def approve_comments(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(request, f'{updated} comentario(s) aprobado(s).', messages.SUCCESS)

    @admin.action(description='Desactivar comentarios seleccionados')
    def deactivate_comments(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, f'{updated} comentario(s) desactivado(s).', messages.WARNING)
