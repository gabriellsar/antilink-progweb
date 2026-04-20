from django.contrib import admin
from django.urls import path, include
import django.contrib.auth.views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'contas/login/', 
        auth_views.LoginView.as_view(template_name='usuarios/registration/login.html'), 
        name='login'
    ),

    path('contas/', include('django.contrib.auth.urls')),
    
    # usuários/urls.py 
    path('usuarios/', include('usuarios.urls')),

    # mural/urls.py
    path('', include('mural.urls')),
]