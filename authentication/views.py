from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages

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
