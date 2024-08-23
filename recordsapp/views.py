from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from .models import Visitante, Categoria, Status
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse

def search_visitantes(request):
    if request.method=='POST':
        search_str = json.loads(request.body).get('searchText')

        visitantes = Visitante.objects.filter(
            nome__icontains = search_str, creator = request.user) | Visitante.objects.filter(
            cpf__istartswith = search_str, creator = request.user) | Visitante.objects.filter(
            categoria__icontains = search_str, creator = request.user) | Visitante.objects.filter(
            empresa__icontains = search_str, creator = request.user) | Visitante.objects.filter(
            placa__istartswith = search_str, creator = request.user) | Visitante.objects.filter(
            hora__istartswith = search_str, creator = request.user) | Visitante.objects.filter(
            data__icontains = search_str, creator = request.user) | Visitante.objects.filter(
            status__icontains=search_str,creator = request.user)
        
        data = visitantes.values()
        return JsonResponse(list(data), safe=False)   



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/authentication/login')
def index(request):
    categorias = Categoria.objects.all()
    status = Status.objects.all()
    visitantes = Visitante.objects.filter(creator = request.user)
    paginator = Paginator(visitantes, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'visitantes': visitantes,
        'page_obj': page_obj
    }
    return render(request,'records/index.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/authentication/login')
def add_record(request):
    # Adicionar aqui o condicional que limita os status dependendo do grupo de usuário
    categorias = Categoria.objects.all()
    status = Status.objects.all()
    context = {
        'categorias': categorias,
        'status': status,
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request,'records/add_record.html', context)
    

    if request.method == 'POST':
        nome_visitante = request.POST['nome_visitante']
        cpf_visitante = request.POST['cpf_visitante']
        categoria_visitante = request.POST['categoria_visitante']
        empresa_visitante = request.POST['empresa_visitante']
        placa_visitante = request.POST['placa_visitante']
        hora_visitante = request.POST['hora_visitante']
        data_visitante = request.POST['data_visitante']
        status_visitante = request.POST['status_visitante']



        if not nome_visitante:
            messages.error(request, 'É necessário informar o nome completo')
            return render(request,'records/add_record.html', context)
    
        if not cpf_visitante:
            messages.error(request, 'É necessário informar o CPF')
            return render(request,'records/add_record.html', context)
        
        if not categoria_visitante:
            messages.error(request, 'É necessário informar a categoria')
            return render(request,'records/add_record.html', context)
        
        if not hora_visitante:
            messages.error(request, 'É necessário informar o horário')
            return render(request,'records/add_record.html', context)
        
        if not data_visitante:
            messages.error(request, 'É necessário informar a data')
            return render(request,'records/add_record.html', context)
        
        if not status_visitante:
            messages.error(request, 'É necessário informar o status')
            return render(request,'records/add_record.html', context)
        
        Visitante.objects.create(
            nome = nome_visitante,
            cpf = cpf_visitante,
            categoria = categoria_visitante,
            empresa = empresa_visitante,
            placa = placa_visitante,
            hora = hora_visitante,
            data = data_visitante,
            creator = request.user,
            status = status_visitante
        )

        messages.success(request, 'Registro salvo com sucesso!')

        return redirect('recordsapp')

def visitante_edit(request, id):
    visitantes = Visitante.objects.get(pk=id)
    categorias = Categoria.objects.all()
    status = Status.objects.all()
    context = {
        'visitantes': visitantes,
        'categorias': categorias,
        'status': status,
        'values': visitantes,
    }
    if request.method == 'GET':
        return render(request, 'records/visitante_edit.html', context)
    if request.method == 'POST':
        nome_visitante = request.POST['nome_visitante']
        cpf_visitante = request.POST['cpf_visitante']
        categoria_visitante = request.POST['categoria_visitante']
        empresa_visitante = request.POST['empresa_visitante']
        placa_visitante = request.POST['placa_visitante']
        hora_visitante = request.POST['hora_visitante']
        data_visitante = request.POST['data_visitante']
        status_visitante = request.POST['status_visitante']



        if not nome_visitante:
            messages.error(request, 'É necessário informar o nome completo')
            return render(request,'records/visitante_edit.html', context)
    
        if not cpf_visitante:
            messages.error(request, 'É necessário informar o CPF')
            return render(request,'records/visitante_edit.html', context)
        
        if not categoria_visitante:
            messages.error(request, 'É necessário informar a categoria')
            return render(request,'records/visitante_edit.html', context)
        
        if not hora_visitante:
            messages.error(request, 'É necessário informar o horário')
            return render(request,'records/visitante_edit.html', context)
        
        if not data_visitante:
            messages.error(request, 'É necessário informar a data')
            return render(request,'records/visitante_edit.html', context)
        
        if not status_visitante:
            messages.error(request, 'É necessário informar o status')
            return render(request,'records/visitante_edit.html', context)
        
        visitantes.nome = nome_visitante
        visitantes.cpf = cpf_visitante
        visitantes.categoria = categoria_visitante
        visitantes.empresa = empresa_visitante
        visitantes.placa = placa_visitante
        visitantes.hora = hora_visitante
        visitantes.data = data_visitante
        visitantes.creator = request.user
        visitantes.status = status_visitante

        visitantes.save()
        messages.success(request, 'Registro atualizado com sucesso!')

        return redirect('recordsapp')
    
def visitante_delete(request,id):
    visitantes = Visitante.objects.get(pk=id)
    visitantes.delete()
    messages.success(request, 'Registro removido com sucesso!')
    return redirect('recordsapp')
