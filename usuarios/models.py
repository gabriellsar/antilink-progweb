from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Fracasso(models.Model):
    NIVEIS_VERGONHA = [
        ('LEVE', 'Leve'),
        ('MEDIO', 'Médio'),
        ('CRITICO', 'Crítico'),
        ('FUGA', 'Mudar de Nome e País'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fracassos')
    titulo = models.CharField(max_length=200, help_text="Ex: Deletei o banco de produção")
    descricao = models.TextField(help_text="Chore aqui. O espaço é seguro.")
    nivel_vergonha = models.CharField(max_length=10, choices=NIVEIS_VERGONHA, default='MEDIO')
    data_do_ocorrido = models.DateField()
    aprendizado = models.TextField(default="Nada, vou errar de novo.")

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"

class Comentario(models.Model):
    """
    Modelo para armazenar os pitacos e conselhos inúteis que 
    os outros usuários vão deixar nos fracassos alheios.
    """
    fracasso = models.ForeignKey(Fracasso, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField(help_text="Escreva algo condescendente.")
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.autor.username} em {self.fracasso.titulo}"

class Reacao(models.Model):
    """
    Modelo para rastrear qual botão o usuário clicou para julgar o fracasso.
    A restrição unique_together garante que o cara não reaja 50 vezes no mesmo post.
    """
    TIPOS_REACAO = [
        ('LIKE', 'Gostei (Polegar)'),
        ('RISO', 'Rindo da desgraça'),
        ('FACEPALM', 'Mão na testa'),
        ('APOIO', 'Força, guerreiro'),
        ('SURPRESA', 'Como você fez isso?'),
    ]

    fracasso = models.ForeignKey(Fracasso, on_delete=models.CASCADE, related_name='reacoes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=15, choices=TIPOS_REACAO)

    class Meta:
        unique_together = ('fracasso', 'usuario')