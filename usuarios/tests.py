from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Depoimento

class UsuariosTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.vitima = User.objects.create_user(username='dev_junior', password='password123')
        self.agressor = User.objects.create_user(username='tech_lead', password='password123')

    def test_busca_usuario(self):
        """Testa se a barra de busca encontra usuários pelo nome."""
        self.client.login(username='tech_lead', password='password123')
        response = self.client.get(reverse('buscar_usuarios'), {'q': 'junior'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '@dev_junior')
        # Garante que não traz quem não tem a ver
        self.assertNotContains(response, '@tech_lead')

    def test_adicionar_depoimento(self):
        """Testa se um usuário consegue ofender profissionalmente outro."""
        self.client.login(username='tech_lead', password='password123')
        url = reverse('adicionar_depoimento', args=[self.vitima.username])
        dados = {'texto': 'Sempre esquece de commitar os arquivos de configuração.'}
        
        response = self.client.post(url, dados)
        
        # Verifica o redirect pro perfil
        self.assertEqual(response.status_code, 302)
        
        # Verifica se o depoimento foi salvo corretamente
        depoimento = Depoimento.objects.first()
        self.assertIsNotNone(depoimento)
        self.assertEqual(depoimento.autor, self.agressor)
        self.assertEqual(depoimento.alvo, self.vitima)

    def test_impedir_auto_depoimento(self):
        """Testa se o backend bloqueia um usuário de ofender a si mesmo."""
        self.client.login(username='tech_lead', password='password123')
        
        # O tech_lead tenta forçar um POST na URL do próprio perfil
        url = reverse('adicionar_depoimento', args=[self.agressor.username])
        dados = {'texto': 'Sou o pior Tech Lead do mundo.'}
        
        response = self.client.post(url, dados)
        
        # Verifica se ele foi redirecionado (com a mensagem de erro)
        self.assertEqual(response.status_code, 302)
        
        # O CRUCIAL: Verifica que NENHUM depoimento foi salvo no banco
        self.assertEqual(Depoimento.objects.count(), 0)