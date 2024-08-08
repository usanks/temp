from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth

# Create your views here.

class UsernameValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        username = data['username']    
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'O nome do usuário deve ser composto apenas por letras e números'}, status = 400)
        if User.objects.filter(username = username).exists():
            return JsonResponse({'username_error': 'Desculpe, esse nome de usuário já está em uso. Por favor, escolha outro.'}, status = 409)
        return JsonResponse({'username_valid': True})

class RegistrationView(View):
    def get(self,request):
        return render(request,'authentication/register.html')    
    def post(self,request):
        # Pegando os dados
        username = request.POST['username']
        password = request.POST['password']
        context = {
            'fieldValues': request.POST
        }
        # Validando
        if not User.objects.filter(username=username).exists():
            if len(password) < 6:
                messages.error(request, 'A senha deve conter ao menos 6 caracteres')
                return render(request,'authentication/register.html', context)
            user = User.objects.create_user(username=username)
            user.set_password(password)
            user.save()
            messages.success(request, 'A sua conta foi criada')
            return render(request,'authentication/register.html')
        
class LoginView(View):
    def get(self,request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Bem-vindo, '+user.username+'.')

                    return redirect('recordsapp')
                messages.error(
                    request, 'A conta não existe, por favor solicite a criação de um acesso')
                return render(request, 'authentication/login.html')
            messages.error(
                request, 'Credenciais inválidas, tente novamente')
            return render(request, 'authentication/login.html')
        messages.error(
            request, 'Por favor, preencha todos os campos')
        return render(request, 'authentication/login.html')
    
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'Você foi desconectado')
        return redirect('login')

