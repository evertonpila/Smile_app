from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('home')  # Usando o name da URL
    
    if request.method == "GET":
        return render(request, 'cadastro.html')  # Caminho completo
    
    elif request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not all([nome, email, senha, confirmar_senha]):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return render(request, 'cadastro.html')

        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'Digite duas senhas iguais')
            return render(request, 'cadastro.html')
        
        if User.objects.filter(email=email).exists():
            messages.add_message(request, constants.ERROR, 'E-mail já cadastrado')
            return render(request, 'cadastro.html')

        try:
            user = User.objects.create_user(
                username=nome,
                email=email,
                password=senha,
            )
            messages.add_message(request, constants.SUCCESS, 'Cadastrado com sucesso!')
            return redirect('login')  # Redireciona para login após cadastro
            
        except Exception as e:
            messages.add_message(request, constants.ERROR, f'Erro interno: {str(e)}')
            return render(request, 'cadastro.html')

def logar(request):
    if request.user.is_authenticated:
        return redirect('home')  # Usando o name da URL
    
    if request.method == "GET":
        return render(request, 'login2.html')  # Caminho completo
    
    elif request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=senha)
            
            if user is not None:
                login(request, user)
                return redirect('home')  # Redireciona para a home após login
            else:
                messages.add_message(request, constants.ERROR, 'Credenciais inválidas')
                return render(request, 'login2.html')
        
        except User.DoesNotExist:
            messages.add_message(request, constants.ERROR, 'Usuário não encontrado')
            return render(request, 'login2.html')

def sair(request):
    logout(request)
    return redirect('login')  # Redireciona para login após logout