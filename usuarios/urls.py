from django.urls import path
from .views import (
    CadastroView, PerfilPublicoView, 
    AdicionarDepoimentoView, BuscarUsuariosView
)

urlpatterns = [
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('buscar/', BuscarUsuariosView.as_view(), name='buscar_usuarios'),
    path('<str:username>/', PerfilPublicoView.as_view(), name='perfil_publico'),
    path('<str:username>/recomendar/', AdicionarDepoimentoView.as_view(), name='adicionar_depoimento'),
]