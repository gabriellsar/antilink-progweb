import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from mural.models import Fracasso, Comentario, Reacao
from usuarios.models import Depoimento

class Command(BaseCommand):
    help = 'Popula o banco de dados do Anti-LinkedIn com incompetência artificial 100% brasileira.'

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')
        
        self.stdout.write(self.style.WARNING('Deletando os vestígios da última catástrofe (Limpando banco)...'))
        Depoimento.objects.all().delete()
        Reacao.objects.all().delete()
        Comentario.objects.all().delete()
        Fracasso.objects.all().delete()
        User.objects.filter(is_superuser=False).delete() 

        titulos_reais = [
            "Esqueci o WHERE no UPDATE",
            "Fiz commit com a senha do banco",
            "Vazei a chave da AWS no GitHub",
            "Derrubei o servidor de produção na sexta 18h",
            "Rodei rm -rf / no diretório errado",
            "Achei que o backup tava rodando (não tava)",
            "Criei um loop infinito que custou 500 dólares",
            "Deixei um console.log('socorro') em prod"
        ]

        descricoes_reais = [
            "Fui fazer um hotfix rapidinho direto na master. O código compilou, mas o servidor pegou fogo logo em seguida.",
            "Copiei uma solução do StackOverflow de 2014 que usava uma biblioteca depreciada. Ninguém revisou o PR.",
            "Testei no localhost e rodou liso. Quando subiu pra nuvem, derrubou até o sistema de ar condicionado da empresa.",
            "Era só pra atualizar um campo na tabela. Eu esqueci o bendito do WHERE. Agora todos os usuários do sistema se chamam 'Teste'."
        ]

        aprendizados = [
            "Sexta-feira é dia de read-only.",
            "Nunca mais confio num indiano do YouTube.",
            "O botão de deploy não é um brinquedo.",
            "Backup que não é testado é só uma promessa.",
            "Nada, amanhã eu cometo o mesmo erro de novo."
        ]

        comentarios_toxicos = [
            "Sênior de 2 anos é assim mesmo...",
            "Na minha máquina funcionou perfeitamente.",
            "Padrão de qualidade impressionante. Continua assim!",
            "Incrível como o RH aprovou sua contratação.",
            "LGTB: Looks Good To Bypass (Aprovado sem olhar).",
            "Pivota pra agronomia, cara. Programação não é pra você."
        ]

        ofensas_profissionais = [
            "Excelente profissional! Recomendo fortemente para a equipe dos meus concorrentes.",
            "Trabalha muito bem sob pressão. Principalmente porque é ele quem cria a pressão na equipe.",
            "Seu código é como uma poesia moderna: impossível de entender na primeira leitura e te faz chorar.",
            "Um verdadeiro pioneiro: ele cria bugs que a linguagem de programação nem sabia que suportava."
        ]

        self.stdout.write(self.style.SUCCESS('Criando novos sofredores (Usuários)...'))
        usuarios = []
        for _ in range(12): 
            # Faker apenas para nomes reais e e-mails
            user = User.objects.create_user(
                username=fake.user_name(),
                first_name=fake.first_name(),
                email=fake.email(),
                password='senha_fraca_123'
            )
            usuarios.append(user)

        self.stdout.write(self.style.SUCCESS('Gerando Fracassos Históricos...'))
        niveis = ['LEVE', 'MEDIO', 'CRITICO', 'FUGA']
        fracassos = []
        for _ in range(30): 
            fracasso = Fracasso.objects.create(
                usuario=random.choice(usuarios),
                titulo=random.choice(titulos_reais),
                descricao=random.choice(descricoes_reais),
                nivel_vergonha=random.choice(niveis),
                data_do_ocorrido=fake.date_between(start_date='-1y', end_date='today'),
                aprendizado=random.choice(aprendizados)
            )
            fracassos.append(fracasso)

        self.stdout.write(self.style.SUCCESS('Distribuindo Reações e Comentários Tóxicos...'))
        tipos_reacao = ['LIKE', 'RISO', 'FACEPALM', 'APOIO', 'SURPRESA']
        
        for fracasso in fracassos:
            # Reações 
            usuarios_reagentes = random.sample(usuarios, random.randint(0, 8))
            for u in usuarios_reagentes:
                Reacao.objects.create(
                    fracasso=fracasso,
                    usuario=u,
                    tipo=random.choice(tipos_reacao)
                )
            
            # Comentários
            for _ in range(random.randint(0, 3)):
                Comentario.objects.create(
                    fracasso=fracasso,
                    autor=random.choice(usuarios),
                    texto=random.choice(comentarios_toxicos)
                )

        self.stdout.write(self.style.SUCCESS('Falsificando Endossos de Incompetência...'))
        for alvo in usuarios:
            autores = random.sample([u for u in usuarios if u != alvo], random.randint(0, 2))
            for autor in autores:
                Depoimento.objects.create(
                    autor=autor,
                    alvo=alvo,
                    texto=random.choice(ofensas_profissionais)
                )

        self.stdout.write(self.style.SUCCESS('Pronto! O abismo corporativo foi populado em PT-BR com sucesso. 🚀'))