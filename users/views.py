from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_fmk
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse('Nome de usuário não disponível.')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return HttpResponse('Cadastro realizado.')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login_fmk(request, user)
            return redirect('home_page')  # Redireciona para a view home_page
        else:
            return HttpResponse('Nome de usuário ou senha incorretos!')

@login_required(login_url='/auth/login/')
def home_page(request):
    return render(request, 'incomes.html')  # Renderiza a página HTML
