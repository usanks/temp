from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib import auth

# Create your views here.
    
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
            messages.error(request, 'Credenciais inválidas, tente novamente')
            return render(request, 'authentication/login.html')
        messages.error(request, 'Por favor, preencha todos os campos')
        return render(request, 'authentication/login.html')
    
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'Você foi desconectado')
        return redirect('login')

