from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Fracasso, Reacao

class MuralTestCase(TestCase):
    def setUp(self):
        """Prepara o ambiente antes de cada teste rodar."""
        self.client = Client()
        
        # Criamos dois usuários de teste
        self.user1 = User.objects.create_user(username='incompetente1', password='password123')
        self.user2 = User.objects.create_user(username='incompetente2', password='password123')
        
        # Criamos um fracasso base
        self.fracasso = Fracasso.objects.create(
            usuario=self.user1,
            titulo='Derrubei a base de dados',
            descricao='Fiz um UPDATE sem WHERE.',
            nivel_vergonha='CRITICO',
            data_do_ocorrido='2024-01-01'
        )

    def test_feed_global_protegido(self):
        """Garante que usuários não logados sejam redirecionados para o login."""
        response = self.client.get(reverse('feed_global'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/contas/login/', response.url)

    def test_feed_global_acesso_permitido(self):
        """Garante que usuários logados consigam ver o feed."""
        self.client.login(username='incompetente1', password='password123')
        response = self.client.get(reverse('feed_global'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Derrubei a base de dados')

    def test_criar_fracasso(self):
        """Testa se um usuário consegue assumir a culpa de um novo erro."""
        self.client.login(username='incompetente2', password='password123')
        dados = {
            'titulo': 'Esqueci o print no código',
            'descricao': 'Subi print("aqui") pra prod',
            'nivel_vergonha': 'LEVE',
            'data_do_ocorrido': '2024-01-02',
            'aprendizado': 'Nenhum'
        }
        response = self.client.post(reverse('assumir_culpa'), dados)
        
        # Verifica se redirecionou pro feed com sucesso
        self.assertEqual(response.status_code, 302)
        
        # Verifica se o fracasso foi salvo no banco e pertence ao user2
        novo_fracasso = Fracasso.objects.get(titulo='Esqueci o print no código')
        self.assertEqual(novo_fracasso.usuario, self.user2)

    def test_alternar_reacao(self):
        """Testa a lógica de adicionar e remover a mesma reação."""
        self.client.login(username='incompetente2', password='password123')
        url = reverse('alternar_reacao', args=[self.fracasso.id])
        
        # 1. Dá um LIKE (deve criar a reação)
        self.client.post(url, {'tipo': 'LIKE'}, HTTP_REFERER='/')
        self.assertEqual(Reacao.objects.filter(fracasso=self.fracasso, usuario=self.user2).count(), 1)
        
        # 2. Clica no LIKE de novo (deve remover a reação)
        self.client.post(url, {'tipo': 'LIKE'}, HTTP_REFERER='/')
        self.assertEqual(Reacao.objects.filter(fracasso=self.fracasso, usuario=self.user2).count(), 0)
        
        # 3. Muda de ideia e manda um FACEPALM (deve criar nova reação)
        self.client.post(url, {'tipo': 'FACEPALM'}, HTTP_REFERER='/')
        reacao = Reacao.objects.get(fracasso=self.fracasso, usuario=self.user2)
        self.assertEqual(reacao.tipo, 'FACEPALM')