from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Cliente, Endereco


class CadastroClienteForm(UserCreationForm):
    """US16 - Criar conta"""
    nome = forms.CharField(
        max_length=150,
        label='Nome completo',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Seu nome completo'
        })
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'seu@email.com'
        })
    )
    cpf = forms.CharField(
        max_length=14,
        label='CPF',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '000.000.000-00',
            'maxlength': '14',
            'data-mask': '000.000.000-00',
        })
    )
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Mínimo 8 caracteres'
        })
    )
    password2 = forms.CharField(
        label='Confirme a senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Repita a senha'
        })
    )

    class Meta:
        model = Cliente
        fields = ('nome', 'email', 'cpf', 'password1', 'password2')

    def clean_cpf(self):
        import re
        cpf = self.cleaned_data['cpf']
        nums = re.sub(r'\D', '', cpf)
        if len(nums) != 11:
            raise forms.ValidationError('CPF deve ter 11 dígitos.')
        if Cliente.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError('Este CPF já está cadastrado.')
        return cpf

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if Cliente.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está cadastrado.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.nome = self.cleaned_data['nome']
        user.email = self.cleaned_data['email']
        user.cpf = self.cleaned_data['cpf']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """US17 - Fazer login"""
    username = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'seu@email.com',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Sua senha',
        })
    )
    
class EnderecoForm(forms.ModelForm):
    """US14 - Informar endereço de entrega"""
    class Meta:
        model = Endereco
        fields = ['cep', 'logradouro', 'numero', 'complemento',
                  'bairro', 'cidade', 'estado', 'principal']
        widgets = {
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000-000'}),
            'logradouro': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 2}),
        }