from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from TradingGame.models import Stock, History
from django.core import serializers
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from TradingGame.forms import SetupForm, AdviseSetupForm
from django.shortcuts import render_to_response

class SignUpForm(UserCreationForm): 
	username = forms.Field(widget=forms.TextInput(attrs={'placeholder': '用戶名'})) 
	email = forms.Field(widget=forms.EmailInput(attrs={'placeholder':'電子郵件'})) 
	password1 = forms.Field(widget=forms.PasswordInput(attrs={'placeholder':'密碼'})) 
	password2 = forms.Field(widget=forms.PasswordInput(attrs={'placeholder':'密碼確認'})) 

	class Meta: 
		model = User  
		fields = ('username','email','password1','password2') 


def home(request):
	return render(request, 'home.html', {'userName': '陳宇鑫'})

def aboutMe(request):
	return render(request, 'aboutMe.html')

def developmentTeam(request):
	return render(request, 'developmentTeam.html')

def setup(request):
    form = SetupForm(request.POST or None)
    if form.is_valid():
        setup = form.save(commit=False)
        setup.user = request.user
        setup.save()
        stock = Stock.objects.get(code = setup.stock_code, date = setup.initial_transaction_date)
        history = History.objects.create(setup = setup, day = 0, action = 0,
            position_after_action = '現金', rate_of_return_after_action = 0, 
            cash_held_after_action = setup.principal, number_of_shares_held_after_action = 0)
        history.day = 1
        return render(request, 'playing.html', {'stock': stock, 'setup': setup, 'history': history})

    return render(request, 'setup.html', {'form': form})

def history(request):
    historys = History.objects.all()
    return render(request, 'history.html', {'historys': historys})

def intelligentInvestmentAdvise(request):
	stock = Stock.objects.get(pk = 1)

	form = AdviseSetupForm(request.POST or None)
	if form.is_valid():
		setup = form.save(commit=False)
		setup.user = request.user
		setup.save()

	return render(request, 'intelligentInvestmentAdvise.html', {'stock': stock, 'form':form})

def stockDay(request):
    stockId = request.POST.get('id')
    stock = Stock.objects.filter(pk = int(stockId)+1)
    stock_list = serializers.serialize('json', stock)

    # 神經網路
    # 讀神經網路的參數
    #...
    #神經網路當天的決定
    return HttpResponse(stock_list, content_type="text/json-comment-filtered")

def addingHistory_waitOrHold(request):
    history_id = request.POST.get('historyId')
    history = History.objects.get(pk = history_id)

    history_new = History.objects.create(
        setup = history.setup,
        day = int(history.day) + 1, 
        action = 0,
        position_after_action = history.position_after_action, 
        last_trading_price_after_action = history.last_trading_price_after_action,
        rate_of_return_after_action = history.rate_of_return_after_action, 
        cash_held_after_action = history.cash_held_after_action,
        number_of_shares_held_after_action = history.number_of_shares_held_after_action
    )
    print(history_new.position_after_action)
    history = History.objects.filter(pk = history_new.id)
    history_list = serializers.serialize('json', history)

    return HttpResponse(history_list, content_type="text/json-comment-filtered")

def addingHistory_buyOrSell(request):
    history_id = request.POST.get('historyId')
    history = History.objects.get(pk = history_id)

    history_list = ''

    if history.position_after_action == '現金':
        history_new = History.objects.create(
            setup = history.setup,
            day = int(history.day) + 1, 
            action = 1,
            position_after_action = '股票', 
            last_trading_price_after_action = 50,
            rate_of_return_after_action = history.rate_of_return_after_action, 
            cash_held_after_action = 0,
            number_of_shares_held_after_action = history.cash_held_after_action / 50
        )
        history = History.objects.filter(pk = history_new.id)
        history_list = serializers.serialize('json', history)

    else:
        history_new = History.objects.create(
            setup = history.setup,
            day = int(history.day) + 1, 
            action = 1,
            position_after_action = '現金', 
            last_trading_price_after_action = 55,
            rate_of_return_after_action = (1 + history.rate_of_return_after_action) * (55 / 50) - 1, 
            cash_held_after_action = history.number_of_shares_held_after_action * 55,
            number_of_shares_held_after_action = 0
        )
        history = History.objects.filter(pk = history_new.id)
        history_list = serializers.serialize('json', history)

    return HttpResponse(history_list, content_type="text/json-comment-filtered")


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
