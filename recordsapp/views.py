from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'records/index.html')

def add_record(request):
    return render(request,'records/add_record.html')

