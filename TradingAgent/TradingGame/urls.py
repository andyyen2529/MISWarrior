from django.conf.urls import url  
from TradingGame.views import setup, playing, playing2#, history

urlpatterns = [ 
	url(r'setup', setup, name = 'setup'),
    url(r'playing', playing, name = 'playing'),
    url(r'playing2', playing2, name = 'playing2'),
    #url(r'history', history), 
]  