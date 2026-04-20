from django.urls import path
from .views import (
    FeedGlobalView, FracassoDeleteView, FracassoListView, FracassoCreateView, 
    AdicionarComentarioView, AlternarReacaoView, FracassoUpdateView
)

urlpatterns = [
    path('', FeedGlobalView.as_view(), name='feed_global'),
    path('meus-fracassos/', FracassoListView.as_view(), name='feed_da_miseria'),
    path('assumir-culpa/', FracassoCreateView.as_view(), name='assumir_culpa'),
    path('<int:fracasso_id>/comentar/', AdicionarComentarioView.as_view(), name='adicionar_comentario'),
    path('<int:fracasso_id>/reagir/', AlternarReacaoView.as_view(), name='alternar_reacao'),

    path('fracasso/<int:pk>/editar/', FracassoUpdateView.as_view(), name='editar_fracasso'),
    path('fracasso/<int:pk>/deletar/', FracassoDeleteView.as_view(), name='deletar_fracasso'),
]