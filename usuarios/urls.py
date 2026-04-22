from django.urls import path
from .views import (
    CadastroView, DeletarContaView, EditarPerfilView, PerfilPublicoView, 
    AdicionarDepoimentoView, BuscarUsuariosView
)

urlpatterns = [
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('buscar/', BuscarUsuariosView.as_view(), name='buscar_usuarios'),
    path('configuracoes/', EditarPerfilView.as_view(), name='editar_perfil'),
    path('deletar-conta/', DeletarContaView.as_view(), name='deletar_conta'),
    path('<str:username>/', PerfilPublicoView.as_view(), name='perfil_publico'),
    path('<str:username>/recomendar/', AdicionarDepoimentoView.as_view(), name='adicionar_depoimento'),
]