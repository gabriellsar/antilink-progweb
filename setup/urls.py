# setup/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # usuários/urls.py 
    path('contas/', include('django.contrib.auth.urls')),
    path('usuarios/', include('usuarios.urls')),

    # mural/urls.py
    path('', include('mural.urls')),
]