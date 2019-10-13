"""TradingAgent URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from TradingGame import views

urlpatterns = [
    url(r'^$', views.home, name = 'home'),
    url(r'^aboutMe/', views.aboutMe, name = 'aboutMe'),
	url(r'^stockGame/', views.setup, name = 'stockGame'),
    url(r'^history/', views.history, name = 'history'),
    #url(r'^playing/', views.playing, name = 'playing'),
    #url(r'^stockGame/', include("TradingGame.urls")),
    url(r'^developmentTeam/', views.developmentTeam, name = 'developmentTeam'),
    url(r'^ajax/stockDay', views.stockDay, name='stockDay'),
    url(r'^ajax/addingHistory', views.addingHistory, name='addingHistory'),
    url(r'^intelligentInvestmentAdvise/', views.intelligentInvestmentAdvise, name = 'intelligentInvestmentAdvise'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/signup/', views.signup, name='signup'),
    url(r'^admin/', admin.site.urls),
]