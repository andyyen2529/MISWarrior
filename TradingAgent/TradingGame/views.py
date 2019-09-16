from django.shortcuts import render
from django.http import HttpResponse
from TradingGame.models import Stock

# def index(request):
#     return HttpResponse("Hello, world. You're 是 887")
	
# def index2(request):
#     return render(request, 'index.html', {'question': 'aaa'})

def home(request):
    return render(request, 'home.html', {'author': '陳宇鑫'})

def stockGame(request):
	stock = Stock.objects.get(pk = 1)
	return render(request, 'stockGame.html', {'stock': stock})
