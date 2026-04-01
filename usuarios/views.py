from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, View
from django.contrib import messages

from .models import Depoimento
from .forms import DepoimentoForm
from mural.models import Fracasso

class CadastroView(CreateView):
    """
    Gerencia o registro de novos usuários na plataforma.
    Utiliza o formulário padrão de criação de usuário do Django.
    """
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'usuarios/cadastro.html' 
    
    def form_valid(self, form):
        """
        Adiciona uma mensagem de sucesso na tela após o cadastro bem-sucedido.
        """
        messages.success(self.request, "Sua conta foi criada. Prepare-se para a decepção.")
        return super().form_valid(form)

class PerfilPublicoView(DetailView):
    """
    Exibe o perfil público de um usuário, listando seus fracassos
    e os depoimentos recebidos de outros colegas.
    """
    model = User
    template_name = 'usuarios/perfil_publico.html'
    context_object_name = 'perfil_usuario'

    def get_object(self):
        """Busca o usuário pela URL usando o 'username' em vez da ID primária."""
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        """Injeta dados extras (fracassos, depoimentos e formulário) no template HTML."""
        context = super().get_context_data(**kwargs)
        context['fracassos'] = Fracasso.objects.filter(usuario=self.object).order_by('-data_do_ocorrido')
        context['depoimentos'] = self.object.depoimentos_recebidos.all().order_by('-data_criacao')
        context['form_depoimento'] = DepoimentoForm()
        return context

class AdicionarDepoimentoView(LoginRequiredMixin, View):
    """
    Processa o envio de um novo depoimento.
    """
    def post(self, request, username):
        alvo = get_object_or_404(User, username=username)
        form = DepoimentoForm(request.POST)
        
        if form.is_valid():
            depoimento = form.save(commit=False)
            depoimento.autor = request.user
            depoimento.alvo = alvo
            depoimento.save()
            messages.success(request, f"Você acabou de afundar um pouco mais a carreira de {alvo.username}.")
        
        return redirect('perfil_publico', username=username)

class BuscarUsuariosView(LoginRequiredMixin, ListView):
    """
    Permite pesquisar usuários cadastrados na plataforma pelo nome.
    """
    model = User
    template_name = 'usuarios/buscar_usuarios.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        """Filtra a lista de usuários com base no parâmetro 'q' passado na barra de busca."""
        query = self.request.GET.get('q')
        if query:
            return User.objects.filter(username__icontains=query)
        return User.objects.none()