from django.db import models
from django.contrib.auth.models import User

class Depoimento(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='depoimentos_feitos')
    alvo = models.ForeignKey(User, on_delete=models.CASCADE, related_name='depoimentos_recebidos')
    texto = models.TextField(help_text="Destrua a reputação desta pessoa com carinho.")
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.autor.username} falando mal de {self.alvo.username}"