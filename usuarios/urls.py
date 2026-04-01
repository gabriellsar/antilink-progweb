from django.urls import path
from .views import CadastroView, PerfilPublicoView, adicionar_depoimento, BuscarUsuariosView

urlpatterns = [
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('buscar/', BuscarUsuariosView.as_view(), name='buscar_usuarios'),
    path('<str:username>/', PerfilPublicoView.as_view(), name='perfil_publico'),
    path('<str:username>/recomendar/', adicionar_depoimento, name='adicionar_depoimento'),
]