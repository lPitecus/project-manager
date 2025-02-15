from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    GENDERS = (
        ("M", "Masculino"),
        ("F", "Feminino"),
        ("NB", "Não Binário"),
        ("O", "Outro"),
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )  # Ligação com o User padrão
    biography = models.TextField(blank=True, null=True)  # Biografia opcional
    birth_date = models.DateField(blank=True, null=True)  # Data de nascimento opcional
    gender = models.CharField(max_length=2, choices=GENDERS, blank=True, null=True)
    avatar = models.ImageField(
        upload_to="avatars/", default="avatars/default.png", blank=True
    )

    def __str__(self):
        return f"Perfil de {self.user.username}"
