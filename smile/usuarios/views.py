from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/adotar')
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if len(nome.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0 or len(confirmar_senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'ㅤPreencha tudo.ㅤ')
            return render(request, 'cadastro.html')

        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR,
                                 'ㅤDigite duas senhas iguais.ㅤ')
            return render(request, 'cadastro.html')
        
        if User.objects.filter(email=email).exists():
            messages.add_message(request, constants.ERROR, 'ㅤE-mail já cadastrado.ㅤ')
            return render(request, 'cadastro.html')

        try:
            user = User.objects.create_user(
                username=nome,
                email=email,
                password=senha,
            )

            messages.add_message(request, constants.SUCCESS,
                                 'Você foi cadastrado com sucesso!')
            return redirect('/auth')
        except:
            messages.add_message(request, constants.ERROR, 'ㅤERRO interno!')
            return render(request, 'cadastro.html')


def logar(request):
    if request.user.is_authenticated:
        return redirect('/adotar')
    
    if request.method == "GET":
        return render(request, 'login2.html')
    
    elif request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=senha)
            
            if user is not None:
                login(request, user)
                return redirect(' ')#colocar a url do index
            else:
                messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
                return render(request, 'login2.html')
        
        except User.DoesNotExist:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
            return render(request, 'login2.html')


def sair(request):
    logout(request)
    return render(request, 'index.html')


    