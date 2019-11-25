from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from TradingGame.models import *
from django.core import serializers
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

import datetime

from TradingGame.forms import SetupForm, AdviseSetupForm
from django.shortcuts import render_to_response
from .DQN import adviseAction, makeDecision

import json

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
    return render(request, 'setup.html', {'form': form})

#SECONDARY VIEW TO RETURN JSON DATA TO USER ****NEW PART****
def playing(request):
    if 'setup' in request.POST:

        # 遊玩之前先把該玩家之前的交易歷史紀錄清除 (這裡示範如何取foreign key object中屬性的方法)
        History.objects.filter(setup__user = request.user).delete() 

        # 根據「交易設定介面」的交易設定建立交易設定的資料
        if 'setup_fromRanking' not in request.POST:
            form = SetupForm(request.POST or None)
            setup = form.save(commit=False)
            setup.user = request.user

            # 根據使用者輸入的股票名稱和交易起始日，找到第一個交易日的股市資料
            # 其中交易起始日如果不是股市的交易日，系統會自動挑選「未來最近的交易日」作為交易起始日
            # 例如2016/01/09不是股市的交易日，系統會自動選取未來最近的交易日，即2016/01/11的股市資料
            stock_firstTradingDay = Stock.objects.filter(
                code = setup.stock_code.code,
                date__range = [setup.initial_transaction_date, setup.initial_transaction_date + datetime.timedelta(days = 2000)]
            ).order_by('date')[0]

            # 將正確的交易起始日更新至交易設定後，保存至資料庫中
            setup.initial_transaction_date = stock_firstTradingDay.date
            setup.save()

        # 根據「股神排行榜」的交易設定建立交易設定的資料
        else: 
            setup = Setup.objects.create(
                user = request.user,
                stock_code = StockCode.objects.get(code = request.POST.get('setup.stock_code')),
                initial_transaction_date = request.POST.get('setup.initial_transaction_date'),
                playing_duration = request.POST.get('setup.playing_duration'),
                principal = request.POST.get('setup.principal'),
                transaction_cost_rate = float(request.POST.get('setup.transaction_cost_rate'))
            )

            stock_firstTradingDay = Stock.objects.get(
                code = StockCode.objects.get(code = request.POST.get('setup.stock_code')),
                date = request.POST.get('setup.initial_transaction_date')
            )
            print(stock_firstTradingDay)
            setup.save()


        # 把交易成本比率乘上100，之後在網頁改用百分比呈現
        transaction_cost_rate = setup.transaction_cost_rate * 100

        # 創建第一筆歷史資料
        history = History.objects.create(setup = setup, day = 0, action = 0,
            position_after_action = '現金', rate_of_return_after_action = 0, 
            cash_held_after_action = setup.principal, number_of_shares_held_after_action = 0,
            position_after_action_robot = '現金', rate_of_return_after_action_robot = 0,
            cash_held_after_action_robot = setup.principal, number_of_shares_held_after_action_robot = 0)
        history.day = 1

        # 根據第一個交易日，取過去前三十個交易日(含第一個交易日)的股市資料，作為一開始畫圖的時候所用
        stockData = Stock.objects.filter(
            code = setup.stock_code.code,
            date__lte = stock_firstTradingDay.date
        ).order_by('-date')[0:30] # lte : <=

        date = []
        price = []

        for v in stockData:
            date.append(v.date)
            price.append(v.closing_price)

        date.reverse()
        price.reverse()

        return render(request, 'playing.html', {'stock': stock_firstTradingDay, 'setup': setup, 'history': history, 
        'date': date, 'price': price, 'transaction_cost_rate': transaction_cost_rate})

    else:
        return redirect('stockGame/setup') # 如果直接輸入遊玩頁面的網址，由於完成交易設定，系統將重新導向交易設定的頁面

def history(request):
    historys = History.objects.filter(setup__user = request.user) # 只取該用戶的交易歷史紀錄
    historys = historys[1:]
    history_list = serializers.serialize('python', historys)
    
    # now extract the inner `fields` dicts
    actual_data = [d['fields'] for d in history_list]

    # and now dump to JSON
    output = json.dumps(actual_data)

    return HttpResponse(output, content_type="text/json-comment-filtered")

def result(request):
    setup_newest = Setup.objects.filter(user = request.user).order_by('-id')[0]
    setup_newest.transaction_cost_rate = setup_newest.transaction_cost_rate * 100

    history_lastDay = History.objects.filter(setup__user = request.user).order_by('-id')[0]
    history_lastDay.rate_of_return_after_action = history_lastDay.rate_of_return_after_action * 100    
    return render(request, 'result.html', {'history_lastDay': history_lastDay, 'setup_newest': setup_newest})



    # else:
    #     return redirect('stockGame/setup') # 如果直接輸入遊玩頁面的網址，由於完成交易設定，系統將重新導向交易設定的頁面



def intelligentInvestmentAdvise(request):
	# Django QuerySet
	# solution for negative index
	# today's data (the newest data)
	stock = Stock.objects.order_by('-id')[0]
	
	form = AdviseSetupForm(request.POST or None)
	if form.is_valid():
		setup = form.save(commit=False)
		setup.user = request.user
		setup.save()
		
		# state variable
		if int(request.POST['principal']) != 0:
			position = 0
		else:
			position = 1
		ratio = 1 # 成對交易比率
		state = [ratio, stock.volumn, stock.turnover, stock.opening_price, 
			stock.high, stock.low, stock.closing_price, position]
		action = adviseAction(state)
		decision = makeDecision(position, action)
		
		# get data for plot
		stockData = Stock.objects.order_by('-id')[0:30]
		data = {}
		for v in stockData:
			data[v.date] = v.closing_price
		date = []
		price = []
		for key, value in data.items():
			date.append(key.strftime("%d-%b-%Y"))
			price.append(float(value))
		# reverse() >> re-order the series (long term to short term)
		date.reverse()
		price.reverse()
	
		return render(request, 'advising.html', {'stock': stock, 'setup': setup, 'date': date, 'price': price, 'decision': decision})
	
	return render(request, 'intelligentInvestmentAdvise.html', {'form': form})

def stockDay(request):
    stockId = request.POST.get('id')
    stock = Stock.objects.filter(pk = int(stockId)+1)
    stock_list = serializers.serialize('json', stock)
    return HttpResponse(stock_list, content_type="text/json-comment-filtered")

def addingHistory_waitOrHold(request):
    history_id = request.POST.get('historyId')
    history = History.objects.get(pk = history_id)

    action = '等待' if history.position_after_action == '現金' else '持有'

    # 電腦模擬投資行動和其相關數據處理
    stockId = request.POST.get('id')
    stock = Stock.objects.get(pk = int(stockId)+1)

    tradingPrice = float(request.POST.get('closingPrice'))
    
    ratio = 1 # 成對交易的比例

    if history.position_after_action_robot == '現金':
        position = 0
    else:
        position = 1
    state = [ratio, stock.volumn, stock.turnover, stock.opening_price, 
        stock.high, stock.low, stock.closing_price, position]

    print(position, adviseAction(state))
    action_robot = makeDecision(position, adviseAction(state))
    print(action_robot)


    if action_robot == '買入':
        position_after_action_robot = '股票'
        last_trading_price_after_action_robot = float(request.POST.get('closingPrice'))
        rate_of_return_after_action_robot = (
            (1 + history.rate_of_return_after_action_robot) * (1 - history.setup.transaction_cost_rate) - 1
        ) 
        cash_held_after_action_robot = 0
        number_of_shares_held_after_action_robot = (
            history.cash_held_after_action_robot / (tradingPrice * (1 + history.setup.transaction_cost_rate))
        )

    elif action_robot == '賣出':
        position_after_action_robot = '現金'
        last_trading_price_after_action_robot = tradingPrice 
        rate_of_return_after_action_robot = (
            (1 + history.rate_of_return_after_action_robot) * (tradingPrice * (1 - history.setup.transaction_cost_rate) 
                / history.last_trading_price_after_action_robot) - 1
        )
        cash_held_after_action_robot = (
            history.number_of_shares_held_after_action_robot * tradingPrice * (1 - history.setup.transaction_cost_rate)
        )
        number_of_shares_held_after_action_robot = 0

    else:
        if action_robot == '等待':
            position_after_action_robot = '現金'
        elif action_robot == '持有':
            position_after_action_robot = '股票'
        last_trading_price_after_action_robot = history.last_trading_price_after_action_robot
        rate_of_return_after_action_robot = history.rate_of_return_after_action_robot 
        cash_held_after_action_robot = history.cash_held_after_action_robot
        number_of_shares_held_after_action_robot = history.number_of_shares_held_after_action_robot


    # 新增歷史紀錄
    history_new = History.objects.create(
        setup = history.setup,
        day = int(history.day) + 1,
        action = action,
        position_after_action = history.position_after_action, 
        last_trading_price_after_action = history.last_trading_price_after_action,
        rate_of_return_after_action = history.rate_of_return_after_action, 
        cash_held_after_action = history.cash_held_after_action,
        number_of_shares_held_after_action = history.number_of_shares_held_after_action,
        action_robot = action_robot,
        position_after_action_robot = history.position_after_action_robot, 
        last_trading_price_after_action_robot = history.last_trading_price_after_action_robot,
        rate_of_return_after_action_robot = history.rate_of_return_after_action_robot, 
        cash_held_after_action_robot = history.cash_held_after_action_robot,
        number_of_shares_held_after_action_robot = history.number_of_shares_held_after_action_robot
    )

    history = History.objects.filter(pk = history_new.id)
    history_list = serializers.serialize('json', history)

    return HttpResponse(history_list, content_type="text/json-comment-filtered")

def addingHistory_buyOrSell(request):
    history_id = request.POST.get('historyId')
    history = History.objects.get(pk = history_id)

    history_list = ''

    # 電腦模擬投資行動和其相關數據處理
    stockId = request.POST.get('id')
    stock = Stock.objects.get(pk = int(stockId)+1)

    tradingPrice = float(request.POST.get('closingPrice'))
    
    ratio = 1 # 成對交易的比例

    if history.position_after_action_robot == '現金':
        position = 0
    else:
        position = 1
    state = [ratio, stock.volumn, stock.turnover, stock.opening_price, 
        stock.high, stock.low, stock.closing_price, position]

    print(position, adviseAction(state))
    action_robot = makeDecision(position, adviseAction(state))
    print(action_robot)

    if action_robot == '買入':
        position_after_action_robot = '股票'
        last_trading_price_after_action_robot = float(request.POST.get('closingPrice'))
        rate_of_return_after_action_robot = (
            (1 + history.rate_of_return_after_action_robot) * (1 - history.setup.transaction_cost_rate) - 1
        ) 
        cash_held_after_action_robot = 0
        number_of_shares_held_after_action_robot = (
            history.cash_held_after_action_robot / (tradingPrice * (1 + history.setup.transaction_cost_rate))
        )

    elif action_robot == '賣出':
        position_after_action_robot = '現金'
        last_trading_price_after_action_robot = tradingPrice 
        rate_of_return_after_action_robot = (
            (1 + history.rate_of_return_after_action_robot) * (tradingPrice * (1 - history.setup.transaction_cost_rate) 
                / history.last_trading_price_after_action_robot) - 1
        )
        cash_held_after_action_robot = (
            history.number_of_shares_held_after_action_robot * tradingPrice * (1 - history.setup.transaction_cost_rate)
        )
        number_of_shares_held_after_action_robot = 0

    else:
        if action_robot == '等待':
            position_after_action_robot = '現金'
        elif action_robot == '持有':
            position_after_action_robot = '股票'
        last_trading_price_after_action_robot = history.last_trading_price_after_action_robot
        rate_of_return_after_action_robot = history.rate_of_return_after_action_robot 
        cash_held_after_action_robot = history.cash_held_after_action_robot
        number_of_shares_held_after_action_robot = history.number_of_shares_held_after_action_robot


    if history.position_after_action == '現金':
        history_new = History.objects.create(
            setup = history.setup,
            day = int(history.day) + 1, 
            action = '買入',
            position_after_action = '股票', 
            last_trading_price_after_action = tradingPrice,
            rate_of_return_after_action = 
                (1 + history.rate_of_return_after_action) * (1 - history.setup.transaction_cost_rate) - 1, 
            cash_held_after_action = 0,
            number_of_shares_held_after_action = 
                history.cash_held_after_action / (tradingPrice * (1 + history.setup.transaction_cost_rate)),
            action_robot = action_robot,
            position_after_action_robot = history.position_after_action_robot, 
            last_trading_price_after_action_robot = history.last_trading_price_after_action_robot,
            rate_of_return_after_action_robot = history.rate_of_return_after_action_robot, 
            cash_held_after_action_robot = history.cash_held_after_action_robot,
            number_of_shares_held_after_action_robot = history.number_of_shares_held_after_action_robot
        )
        history = History.objects.filter(pk = history_new.id)
        history_list = serializers.serialize('json', history)

    else:
        history_new = History.objects.create(
            setup = history.setup,
            day = int(history.day) + 1, 
            action = '賣出',
            position_after_action = '現金', 
            last_trading_price_after_action = tradingPrice,
            rate_of_return_after_action = (
                (1 + history.rate_of_return_after_action) * (tradingPrice * (1 - history.setup.transaction_cost_rate)
                     / history.last_trading_price_after_action) - 1
            ), 
            cash_held_after_action = 
                history.number_of_shares_held_after_action * tradingPrice * (1 - history.setup.transaction_cost_rate),
            number_of_shares_held_after_action = 0,
            action_robot = action_robot,
            position_after_action_robot = history.position_after_action_robot, 
            last_trading_price_after_action_robot = history.last_trading_price_after_action_robot,
            rate_of_return_after_action_robot = history.rate_of_return_after_action_robot, 
            cash_held_after_action_robot = history.cash_held_after_action_robot,
            number_of_shares_held_after_action_robot = history.number_of_shares_held_after_action_robot
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

def addingRankingHistory(request):
	# 取得目前的交易歷史
    history_id = request.POST.get('historyId')
    history = History.objects.get(pk = history_id)
	
    ranking_history_new = RankingHistory.objects.create(
        setup = history.setup,
        final_rate_of_return = history.rate_of_return_after_action
    )
    ranking_history = RankingHistory.objects.filter(pk = ranking_history_new.id)
    ranking_history_list = serializers.serialize('json', ranking_history)

    return HttpResponse(ranking_history_list, content_type="text/json-comment-filtered")



def ranking(request):
    ranking_table = RankingHistory.objects.order_by('-final_rate_of_return')[:10]  # 取前10名

    for i in range(0,len(ranking_table)):
        ranking_table[i].setup.transaction_cost_rate *= 100
        ranking_table[i].final_rate_of_return *= 100

    return render(request, 'ranking.html',{'ranking_table' : ranking_table})
