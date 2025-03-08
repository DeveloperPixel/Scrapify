from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def wip(request):
    return render(request, 'wip.html')
