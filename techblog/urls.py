from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from accounts.forms import StyledAuthenticationForm

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include(('pages.urls', 'pages'), namespace='pages')),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('cuenta/', include(('accounts.urls', 'accounts'), namespace='accounts')),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html',
            authentication_form=StyledAuthenticationForm,
        ),
        name='login',
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# Durante el desarrollo (DEBUG=True), Django sirve los archivos subidos por
# los usuarios (imágenes de posts, avatares) directamente.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
