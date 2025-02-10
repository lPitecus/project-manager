from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # O Django User padrão não exige email, mas podemos tornar obrigatório
    biography = forms.CharField(widget=forms.Textarea, required=False)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    gender = forms.ChoiceField(choices=Profile.GENDERS, required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "biography", "birth_date", "gender"]
