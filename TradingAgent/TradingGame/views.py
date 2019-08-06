from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're 是 87")
	
def index2(request):
    return render(request, 'index.html')