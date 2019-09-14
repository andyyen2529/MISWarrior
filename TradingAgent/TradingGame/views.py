from django.shortcuts import render
from django.http import HttpResponse

# def index(request):
#     return HttpResponse("Hello, world. You're 是 887")
	
# def index2(request):
#     return render(request, 'index.html', {'question': 'aaa'})
	
def stockGame(request):
    return render(request, 'stockGame.html', {'author': '彭琮鈺'})

def home(request):
    return render(request, 'home.html', {'author': '陳宇鑫'})
