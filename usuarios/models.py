from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    titulo = models.CharField(max_length=100, default="Aspirante a Desempregado")
    localizacao = models.CharField(max_length=100, default="Fundo do Poço, Brasil")

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def salvar_perfil_usuario(sender, instance, **kwargs):
    instance.perfil.save()

class Depoimento(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='depoimentos_feitos')
    alvo = models.ForeignKey(User, on_delete=models.CASCADE, related_name='depoimentos_recebidos')
    texto = models.TextField(help_text="Destrua a reputação desta pessoa com carinho.")
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.autor.username} falando mal de {self.alvo.username}"