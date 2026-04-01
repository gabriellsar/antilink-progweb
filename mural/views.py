from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, View

from .models import Comentario, Fracasso, Reacao
from .forms import FracassoForm

class FeedGlobalView(LoginRequiredMixin, ListView):
    """
    Exibe a página inicial do mural, listando os fracassos de todos
    os usuários da plataforma em ordem cronológica reversa.
    """
    model = Fracasso
    template_name = 'mural/feed_global.html'
    context_object_name = 'fracassos'
    
    def get_queryset(self):
        """Retorna todos os fracassos ordenados pelos mais recentes."""
        return Fracasso.objects.all().order_by('-data_do_ocorrido')

class FracassoListView(LoginRequiredMixin, ListView):
    """
    Exibe o feed pessoal do usuário logado,
    contendo apenas os fracassos que ele mesmo publicou.
    """
    model = Fracasso
    template_name = 'mural/feed_da_miseria.html'
    context_object_name = 'fracassos'
    
    def get_queryset(self):
        """Filtra os fracassos para mostrar apenas os do usuário logado."""
        return Fracasso.objects.filter(usuario=self.request.user).order_by('-data_do_ocorrido')

class FracassoCreateView(LoginRequiredMixin, CreateView):
    """
    Gerencia o formulário onde o usuário pode confessar um novo fracasso.
    """
    model = Fracasso
    form_class = FracassoForm
    template_name = 'mural/assumir_culpa.html'
    success_url = reverse_lazy('feed_global')

    def form_valid(self, form):
        """Atribui o usuário logado como autor do fracasso antes de salvar no banco."""
        form.instance.usuario = self.request.user
        messages.success(self.request, "Parabéns! Mais um fracasso registrado com sucesso no seu currículo!")
        return super().form_valid(form)

class AdicionarComentarioView(LoginRequiredMixin, View):
    """
    Processa o envio de um novo comentário em um fracasso específico.
    Apenas aceita requisições POST e redireciona o usuário de volta de onde veio.
    """
    def post(self, request, fracasso_id):
        fracasso = get_object_or_404(Fracasso, id=fracasso_id)
        texto = request.POST.get('texto')
        
        if texto:
            Comentario.objects.create(fracasso=fracasso, autor=request.user, texto=texto)
            messages.success(request, "Comentário registrado com sucesso.")
        
        # Retorna magicamente para a aba/página que o usuário estava
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class AlternarReacaoView(LoginRequiredMixin, View):
    """
    Gerencia o sistema de reações (Like, Riso, Facepalm, etc).
    """
    def post(self, request, fracasso_id):
        fracasso = get_object_or_404(Fracasso, id=fracasso_id)
        tipo = request.POST.get('tipo', 'LIKE')
        
        # Busca se o usuário já reagiu a este fracasso específico
        reacao_existente = Reacao.objects.filter(fracasso=fracasso, usuario=request.user).first()
        
        if reacao_existente:
            if reacao_existente.tipo == tipo:
                reacao_existente.delete() # Clicou na mesma reação, remove
            else:
                reacao_existente.tipo = tipo
                reacao_existente.save()   # Mudou de ideia, atualiza
        else:
            Reacao.objects.create(fracasso=fracasso, usuario=request.user, tipo=tipo)
            
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))