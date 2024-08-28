from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from .models import Fornecedor, Categoria, Status
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
import csv
import datetime

# Create your views here.

def has_group(user, group):
    return user.groups.filter(name=group).exists()

def search_fornecedor(request):
    if has_group(request.user, "guarita"):
        if request.method=='POST':
            search_str = json.loads(request.body).get('searchText')

            fornecedores = Fornecedor.objects.filter(
                nome__icontains = search_str) | Fornecedor.objects.filter(
                cpf__istartswith = search_str) | Fornecedor.objects.filter(
                categoria__icontains = search_str) | Fornecedor.objects.filter(
                empresa__icontains = search_str) | Fornecedor.objects.filter(
                placa__istartswith = search_str) | Fornecedor.objects.filter(
                hora__istartswith = search_str) | Fornecedor.objects.filter(
                data__icontains = search_str) | Fornecedor.objects.filter(
                status__icontains=search_str)
            
            data = fornecedores.values()
            return JsonResponse(list(data), safe=False)
    else:
        if request.method=='POST':
            search_str = json.loads(request.body).get('searchText')

            fornecedores = Fornecedor.objects.filter(
                nome__icontains = search_str, creator = request.user) | Fornecedor.objects.filter(
                cpf__istartswith = search_str, creator = request.user) | Fornecedor.objects.filter(
                categoria__icontains = search_str, creator = request.user) | Fornecedor.objects.filter(
                empresa__icontains = search_str, creator = request.user) | Fornecedor.objects.filter(
                placa__istartswith = search_str, creator = request.user) | Fornecedor.objects.filter(
                hora__istartswith = search_str, creator = request.user) | Fornecedor.objects.filter(
                data__icontains = search_str, creator = request.user) | Fornecedor.objects.filter(
                status__icontains=search_str,creator = request.user)
            
            data = fornecedores.values()
            return JsonResponse(list(data), safe=False)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/authentication/login')
def index(request):
    if has_group(request.user, "guarita"):
        fornecedores = Fornecedor.objects.filter()
        paginator = Paginator(fornecedores, 5)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)
        context = {
            'fornecedores': fornecedores,
            'page_obj': page_obj
        }
        return render(request,'fornecedores/index.html', context)
    else:
        fornecedores = Fornecedor.objects.filter(creator = request.user)
        paginator = Paginator(fornecedores, 5)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)
        context = {
            'fornecedores': fornecedores,
            'page_obj': page_obj
        }
        return render(request,'fornecedores/index.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/authentication/login')
def add_fornecedor(request):
    categorias = Categoria.objects.all()
    status = Status.objects.all()
    context = {
        'categorias': categorias,
        'status': status,
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request,'fornecedores/add_fornecedor.html', context)    

    if request.method == 'POST':
        nome_fornecedor = request.POST['nome_fornecedor']
        cpf_fornecedor = request.POST['cpf_fornecedor']
        categoria_fornecedor = request.POST['categoria_fornecedor']
        empresa_fornecedor = request.POST['empresa_fornecedor']
        placa_fornecedor = request.POST['placa_fornecedor']
        hora_fornecedor = request.POST['hora_fornecedor']
        data_fornecedor = request.POST['data_fornecedor']
        status_fornecedor = request.POST['status_fornecedor']

        if not nome_fornecedor:
            messages.error(request, 'É necessário informar o nome completo')
            return render(request,'fornecedores/add_fornecedor.html', context)
    
        if not cpf_fornecedor:
            messages.error(request, 'É necessário informar o CPF')
            return render(request,'fornecedores/add_fornecedor.html', context)
        
        if not categoria_fornecedor:
            messages.error(request, 'É necessário informar a categoria')
            return render(request,'fornecedores/add_fornecedor.html', context)
        
        if not empresa_fornecedor:
            messages.error(request, 'É necessário informar a empresa')
            return render(request,'servicos/add_servico.html', context)        
        
        if not hora_fornecedor:
            messages.error(request, 'É necessário informar o horário')
            return render(request,'fornecedores/add_fornecedor.html', context)
        
        if not data_fornecedor:
            messages.error(request, 'É necessário informar a data')
            return render(request,'fornecedores/add_fornecedor.html', context)
        
        if not status_fornecedor:
            messages.error(request, 'É necessário informar o status')
            return render(request,'fornecedores/add_fornecedor.html', context)
        
        Fornecedor.objects.create(
            nome = nome_fornecedor,
            cpf = cpf_fornecedor,
            categoria = categoria_fornecedor,
            empresa = empresa_fornecedor,
            placa = placa_fornecedor,
            hora = hora_fornecedor,
            data = data_fornecedor,
            creator = request.user,
            status = status_fornecedor
        )

        messages.success(request, 'Registro salvo com sucesso!')

        return redirect('fornecedor')

def fornecedor_edit(request, id):
    fornecedores = Fornecedor.objects.get(pk=id)
    categorias = Categoria.objects.all()
    status = Status.objects.all()
    context = {
        'fornecedores': fornecedores,
        'categorias': categorias,
        'status': status,
        'values': fornecedores,
    }
    if request.method == 'GET':
        return render(request, 'fornecedores/fornecedor_edit.html', context)
    if request.method == 'POST':
        nome_fornecedor = request.POST['nome_fornecedor']
        cpf_fornecedor = request.POST['cpf_fornecedor']
        categoria_fornecedor = request.POST['categoria_fornecedor']
        empresa_fornecedor = request.POST['empresa_fornecedor']
        placa_fornecedor = request.POST['placa_fornecedor']
        hora_fornecedor = request.POST['hora_fornecedor']
        data_fornecedor = request.POST['data_fornecedor']
        status_fornecedor = request.POST['status_fornecedor']



        if not nome_fornecedor:
            messages.error(request, 'É necessário informar o nome completo')
            return render(request,'fornecedores/fornecedor_edit.html', context)
    
        if not cpf_fornecedor:
            messages.error(request, 'É necessário informar o CPF')
            return render(request,'fornecedores/fornecedor_edit.html', context)
        
        if not categoria_fornecedor:
            messages.error(request, 'É necessário informar a categoria')
            return render(request,'fornecedores/fornecedor_edit.html', context)
        
        if not empresa_fornecedor:
            messages.error(request, 'É necessário informar a empresa')
            return render(request,'fornecedores/fornecedor_edit.html', context)
        
        if not hora_fornecedor:
            messages.error(request, 'É necessário informar o horário')
            return render(request,'fornecedores/fornecedor_edit.html', context)
        
        if not data_fornecedor:
            messages.error(request, 'É necessário informar a data')
            return render(request,'fornecedores/fornecedor_edit.html', context)
        
        if not status_fornecedor:
            messages.error(request, 'É necessário informar o status')
            return render(request,'fornecedores/fornecedor_edit.html', context)
        
        fornecedores.nome = nome_fornecedor
        fornecedores.cpf = cpf_fornecedor
        fornecedores.categoria = categoria_fornecedor
        fornecedores.empresa = empresa_fornecedor
        fornecedores.placa = placa_fornecedor
        fornecedores.hora = hora_fornecedor
        fornecedores.data = data_fornecedor
        fornecedores.status = status_fornecedor

        fornecedores.save()
        messages.success(request, 'Registro atualizado com sucesso!')

        return redirect('fornecedor')       
    
def fornecedor_delete(request,id):
    fornecedores = Fornecedor.objects.get(pk=id)
    fornecedores.delete()
    messages.success(request, 'Registro removido com sucesso!')
    return redirect('fornecedor')

def fornecedor_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition']='attachment; filename = Registros' +str(datetime.datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Nome','CPF','Categoria','Empresa','Placa','Hora','Data','Status'])

    registros = Fornecedor.objects.filter()

    for registro in registros:
        writer.writerow([registro.nome, registro.cpf, registro.categoria, registro.empresa, registro.placa, registro.hora, registro.data, registro.status])
    return response
