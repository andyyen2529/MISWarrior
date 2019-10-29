from django.conf.urls import url  
from TradingGame.views import setup, playing, playing2, ranking, addingRankingHistory #, history

urlpatterns = [ 
	url(r'setup', setup, name = 'setup'),
    url(r'playing', playing, name = 'playing'),
    url(r'playing2', playing2, name = 'playing2'),
	url(r'ranking', ranking, name = 'ranking'),
	url(r'^ajax/addingRankingHistory', addingRankingHistory, name='addingRankingHistory'),
	#url(r'^ajax/addingRankingHistory', views.addingRankingHistory, name='addingRankingHistory'),
    #url(r'history', history), 
]  