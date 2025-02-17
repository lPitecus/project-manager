from django.contrib.auth.management.commands.createsuperuser import (
    Command as BaseCreateSuperUserCommand,
)
from django.contrib.auth import get_user_model
from django.core.management.base import CommandError
from users.models import Profile


class Command(BaseCreateSuperUserCommand):
    def handle(self, *args, **options):
        # Executa o comando original do createsuperuser
        super().handle(*args, **options)

        # Obtém o modelo de usuário definido no projeto
        UserModel = get_user_model()

        # Busca o último superusuário criado
        qs = UserModel.objects.filter(is_superuser=True)
        if qs.exists():
            user = qs.latest("date_joined")
        else:
            raise CommandError(
                "Não foi possível criar um perfil para o superusuário. Nenhum superusuário foi encontrado."
            )

        # Verifica se o perfil já existe, caso contrário, cria um novo
        if not Profile.objects.filter(user=user).exists():
            Profile.objects.get_or_create(user=user)
            self.stdout.write(
                self.style.SUCCESS(
                    f"✔ Perfil criado para o superusuário '{user.username}'."
                )
            )
