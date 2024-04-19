from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages


def sair(request):
    auth.logout(request)
    return redirect('/usuarios/login')


def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = auth.authenticate(request, username=username, password=senha)

        if user:
            auth.login(request, user)
            return redirect('pacientes/home')
        
        messages.add_message(request, messages.constants.ERROR, 'Usuário ou senha incorretos.')
        return redirect('/usuarios/login')


def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        users = User.objects.filter(username=username)

        if users.exists():
            messages.add_message(request, messages.constants.ERROR, 'Usuário já existe!')
            return redirect('/usuarios/cadastro')

        if senha != confirmar_senha:
            messages.add_message(request, messages.constants.ERROR, 'A senha de confirmação deve ser igual a senha digitada.')
            return redirect('/usuarios/cadastro')
        
        if len(senha) < 6:
            messages.add_message(request, messages.constants.ERROR, 'A senha deve possuir mais de 6 digitos.')
            return redirect('/usuarios/cadastro')
        
        try:
            User.objects.create_user(
                username=username,
                email=email,
                password=senha
            )

            return redirect('/usuarios/login')
        
        except Exception: 
            messages.add_message(request, messages.constants.ERROR, 'Não foi possível criar o usuário.')
            return redirect('/usuarios/cadastro')