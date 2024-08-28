from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from .models import Prestador, Categoria, Status
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
import csv
import datetime

# Create your views here.

def has_group(user, group):
    return user.groups.filter(name=group).exists()

def search_servico(request):
    if has_group(request.user, "guarita"):
        if request.method=='POST':
            search_str = json.loads(request.body).get('searchText')

            prestadores = Prestador.objects.filter(
                nome__icontains = search_str) | Prestador.objects.filter(
                cpf__istartswith = search_str) | Prestador.objects.filter(
                categoria__icontains = search_str) | Prestador.objects.filter(
                empresa__icontains = search_str) | Prestador.objects.filter(
                placa__istartswith = search_str) | Prestador.objects.filter(
                hora__istartswith = search_str) | Prestador.objects.filter(
                data__icontains = search_str) | Prestador.objects.filter(
                status__icontains=search_str)
            
            data = prestadores.values()
            return JsonResponse(list(data), safe=False)
    else:
        if request.method=='POST':
            search_str = json.loads(request.body).get('searchText')

            prestadores = Prestador.objects.filter(
                nome__icontains = search_str, creator = request.user) | Prestador.objects.filter(
                cpf__istartswith = search_str, creator = request.user) | Prestador.objects.filter(
                categoria__icontains = search_str, creator = request.user) | Prestador.objects.filter(
                empresa__icontains = search_str, creator = request.user) | Prestador.objects.filter(
                placa__istartswith = search_str, creator = request.user) | Prestador.objects.filter(
                hora__istartswith = search_str, creator = request.user) | Prestador.objects.filter(
                data__icontains = search_str, creator = request.user) | Prestador.objects.filter(
                status__icontains=search_str,creator = request.user)
            
            data = prestadores.values()
            return JsonResponse(list(data), safe=False)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/authentication/login')
def index(request):
    if has_group(request.user, "guarita"):
        prestadores = Prestador.objects.filter()
        paginator = Paginator(prestadores, 5)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)
        context = {
            'prestadores': prestadores,
            'page_obj': page_obj
        }
        return render(request,'servicos/index.html', context)
    else:
        prestadores = Prestador.objects.filter(creator = request.user)
        paginator = Paginator(prestadores, 5)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)
        context = {
            'prestadores': prestadores,
            'page_obj': page_obj
        }
        return render(request,'servicos/index.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/authentication/login')
def add_servico(request):
    categorias = Categoria.objects.all()
    status = Status.objects.all()
    context = {
        'categorias': categorias,
        'status': status,
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request,'servicos/add_servico.html', context)
    

    if request.method == 'POST':
        nome_servico = request.POST['nome_servico']
        cpf_servico = request.POST['cpf_servico']
        categoria_servico = request.POST['categoria_servico']
        empresa_servico = request.POST['empresa_servico']
        placa_servico = request.POST['placa_servico']
        hora_servico = request.POST['hora_servico']
        data_servico = request.POST['data_servico']
        status_servico = request.POST['status_servico']



        if not nome_servico:
            messages.error(request, 'É necessário informar o nome completo')
            return render(request,'servicos/add_servico.html', context)
    
        if not cpf_servico:
            messages.error(request, 'É necessário informar o CPF')
            return render(request,'servicos/add_servico.html', context)
        
        if not categoria_servico:
            messages.error(request, 'É necessário informar a categoria')
            return render(request,'servicos/add_servico.html', context)
        
        if not empresa_servico:
            messages.error(request, 'É necessário informar a empresa')
            return render(request,'servicos/add_servico.html', context)
        
        if not hora_servico:
            messages.error(request, 'É necessário informar o horário')
            return render(request,'servicos/add_servico.html', context)
        
        if not data_servico:
            messages.error(request, 'É necessário informar a data')
            return render(request,'servicos/add_servico.html', context)
        
        if not status_servico:
            messages.error(request, 'É necessário informar o status')
            return render(request,'servicos/add_servico.html', context)
        
        Prestador.objects.create(
            nome = nome_servico,
            cpf = cpf_servico,
            categoria = categoria_servico,
            empresa = empresa_servico,
            placa = placa_servico,
            hora = hora_servico,
            data = data_servico,
            creator = request.user,
            status = status_servico
        )

        messages.success(request, 'Registro salvo com sucesso!')

        return redirect('servico')

def servico_edit(request, id):
    prestadores = Prestador.objects.get(pk=id)
    categorias = Categoria.objects.all()
    status = Status.objects.all()
    context = {
        'prestadores': prestadores,
        'categorias': categorias,
        'status': status,
        'values': prestadores,
    }
    if request.method == 'GET':
        return render(request, 'servicos/servico_edit.html', context)
    if request.method == 'POST':
        nome_servico = request.POST['nome_servico']
        cpf_servico = request.POST['cpf_servico']
        categoria_servico = request.POST['categoria_servico']
        empresa_servico = request.POST['empresa_servico']
        placa_servico = request.POST['placa_servico']
        hora_servico = request.POST['hora_servico']
        data_servico = request.POST['data_servico']
        status_servico = request.POST['status_servico']

        if not nome_servico:
            messages.error(request, 'É necessário informar o nome completo')
            return render(request,'servicos/servico_edit.html', context)
    
        if not cpf_servico:
            messages.error(request, 'É necessário informar o CPF')
            return render(request,'servicos/servico_edit.html', context)
        
        if not categoria_servico:
            messages.error(request, 'É necessário informar a categoria')
            return render(request,'servicos/servico_edit.html', context)
        
        if not empresa_servico:
            messages.error(request, 'É necessário informar a empresa')
            return render(request,'servicos/servico_edit.html', context)
        
        if not hora_servico:
            messages.error(request, 'É necessário informar o horário')
            return render(request,'servicos/servico_edit.html', context)
        
        if not data_servico:
            messages.error(request, 'É necessário informar a data')
            return render(request,'servicos/servico_edit.html', context)
        
        if not status_servico:
            messages.error(request, 'É necessário informar o status')
            return render(request,'servicos/servico_edit.html', context)
        
        prestadores.nome = nome_servico
        prestadores.cpf = cpf_servico
        prestadores.categoria = categoria_servico
        prestadores.empresa = empresa_servico
        prestadores.placa = placa_servico
        prestadores.hora = hora_servico
        prestadores.data = data_servico
        prestadores.status = status_servico

        prestadores.save()
        messages.success(request, 'Registro atualizado com sucesso!')

        return redirect('servico')
    
def servico_delete(request,id):
    prestadores = Prestador.objects.get(pk=id)
    prestadores.delete()
    messages.success(request, 'Registro removido com sucesso!')
    return redirect('servico')

def export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition']='attachment; filename = Registros' +str(datetime.datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Nome','CPF','Categoria','Empresa','Placa','Hora','Data','Status'])

    registros = Prestador.objects.filter()

    for registro in registros:
        writer.writerow([registro.nome, registro.cpf, registro.categoria, registro.empresa, registro.placa, registro.hora, registro.data, registro.status])
    return response