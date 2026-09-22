from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('nueva/', views.PostCreateView.as_view(), name='post_create'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<slug:slug>/editar/', views.PostUpdateView.as_view(), name='post_update'),
    path('<slug:slug>/eliminar/', views.PostDeleteView.as_view(), name='post_delete'),
    path('<slug:slug>/comentar/', views.add_comment, name='add_comment'),
]
