from django.conf.urls import url  
from TradingGame.views import *

urlpatterns = [ 
	url(r'setup', setup, name = 'setup'),
    url(r'playing', playing, name = 'playing'),
	url(r'ranking', ranking, name = 'ranking'),
	url(r'result', result, name = 'result'),
	url(r'^ajax/addingRankingHistory', addingRankingHistory, name='addingRankingHistory'),
]  