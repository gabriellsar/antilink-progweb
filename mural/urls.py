from django.urls import path
from .views import (
    FeedGlobalView, FracassoListView, FracassoCreateView, 
    AdicionarComentarioView, AlternarReacaoView
)

urlpatterns = [
    path('', FeedGlobalView.as_view(), name='feed_global'),
    path('meus-fracassos/', FracassoListView.as_view(), name='feed_da_miseria'),
    path('assumir-culpa/', FracassoCreateView.as_view(), name='assumir_culpa'),
    path('<int:fracasso_id>/comentar/', AdicionarComentarioView.as_view(), name='adicionar_comentario'),
    path('<int:fracasso_id>/reagir/', AlternarReacaoView.as_view(), name='alternar_reacao'),
]