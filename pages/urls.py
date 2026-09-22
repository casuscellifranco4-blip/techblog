from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('acerca-de/', views.about, name='about'),
    path('contacto/', views.contact, name='contact'),
]
