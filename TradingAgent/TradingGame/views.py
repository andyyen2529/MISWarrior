from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from TradingGame.models import Stock
from django.core import serializers
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

def home(request):
    return render(request, 'home.html', {'userName': '陳宇鑫'})

def aboutMe(request):
    return render(request, 'aboutMe.html')

def developmentTeam(request):
    return render(request, 'developmentTeam.html')

def stockGame(request):
	stock = Stock.objects.get(pk = 1)
	return render(request, 'stockGame.html', {'stock': stock})
    
def stockDay(request):
    print(request.POST.get('day'))
    stockId = request.POST.get('id')
    stock = Stock.objects.filter(pk = int(stockId)+1)
    stock_list = serializers.serialize('json', stock)
    print(stock_list)
    return HttpResponse(stock_list, content_type="text/json-comment-filtered")

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})