from django.urls import path
from .views import (
    FeedGlobalView, FracassoListView, FracassoCreateView, 
    adicionar_comentario, alternar_reacao
)

urlpatterns = [
    # A raiz do mural será o feed global
    path('', FeedGlobalView.as_view(), name='feed_global'),
    path('meus-fracassos/', FracassoListView.as_view(), name='feed_da_miseria'),
    path('assumir-culpa/', FracassoCreateView.as_view(), name='assumir_culpa'),
    path('<int:fracasso_id>/comentar/', adicionar_comentario, name='adicionar_comentario'),
    path('<int:fracasso_id>/reagir/', alternar_reacao, name='alternar_reacao'),
]