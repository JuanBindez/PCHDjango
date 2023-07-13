from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from django import forms
from .models import Cliente
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    # Adicione campos extras para o modelo de cliente personalizado
    class Meta:
        model = Cliente
        fields = ('nome', 'email', 'password1', 'password2', 'genero', 'endereco', 'referencia', 'cidade', 'telefone')
