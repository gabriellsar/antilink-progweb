# mural/views.py
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .models import Comentario, Fracasso, Reacao
from .forms import FracassoForm

class FeedGlobalView(LoginRequiredMixin, ListView):
    model = Fracasso
    template_name = 'mural/feed_global.html'
    context_object_name = 'fracassos'
    
    def get_queryset(self):
        return Fracasso.objects.all().order_by('-data_do_ocorrido')

class FracassoListView(LoginRequiredMixin, ListView):
    model = Fracasso
    template_name = 'mural/feed_da_miseria.html'
    context_object_name = 'fracassos'
    
    def get_queryset(self):
        return Fracasso.objects.filter(usuario=self.request.user).order_by('-data_do_ocorrido')

class FracassoCreateView(LoginRequiredMixin, CreateView):
    model = Fracasso
    form_class = FracassoForm
    template_name = 'mural/assumir_culpa.html'
    success_url = reverse_lazy('feed_global')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, "Parabéns! Mais um fracasso registrado com sucesso no seu currículo!")
        return super().form_valid(form)

@login_required
def adicionar_comentario(request, fracasso_id):
    fracasso = get_object_or_404(Fracasso, id=fracasso_id)
    if request.method == 'POST':
        texto = request.POST.get('texto')
        if texto:
            Comentario.objects.create(fracasso=fracasso, autor=request.user, texto=texto)
            messages.success(request, "Pitaco registrado com sucesso.")
    
    # Retorna para a aba/página que o usuário estava
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def alternar_reacao(request, fracasso_id):
    fracasso = get_object_or_404(Fracasso, id=fracasso_id)
    if request.method == 'POST':
        tipo = request.POST.get('tipo', 'LIKE')
        reacao_existente = Reacao.objects.filter(fracasso=fracasso, usuario=request.user).first()
        
        if reacao_existente:
            if reacao_existente.tipo == tipo:
                reacao_existente.delete() # Clicou no mesmo, remove a reação
            else:
                reacao_existente.tipo = tipo # Clicou em outro, atualiza
                reacao_existente.save()
        else:
            Reacao.objects.create(fracasso=fracasso, usuario=request.user, tipo=tipo)
            
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))