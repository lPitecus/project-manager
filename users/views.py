from django.contrib import messages
from django.shortcuts import render, redirect

from users.models import Profile
from .forms import UserRegisterForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # Salva o usuário no banco
            # Ensure the profile exists
            Profile.objects.get_or_create(user=user)
            # Atualiza os campos do perfil
            user.profile.bio = form.cleaned_data["biography"]
            user.profile.birth_date = form.cleaned_data["birth_date"]
            user.profile.gender = form.cleaned_data["gender"]
            user.profile.avatar = form.cleaned_data["avatar"]
            user.profile.save()

            messages.success(
                request,
                f"Conta criada para {user.username}! Agora você pode fazer login.",
            )
            return redirect("users:login")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})
