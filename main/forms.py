from django import forms
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    class Meta:
        model = UserCreationForm.Meta.model  # Используем модель по умолчанию
        fields = UserCreationForm.Meta.fields