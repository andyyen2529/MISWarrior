from django.forms import ModelForm
from TradingGame.models import Setup, AdviseSetup
from django import forms
from django.forms.widgets import TextInput
from django.contrib.admin.widgets import AdminDateWidget

class NumberInput(TextInput):
    input_type = 'number'

class DateInput(forms.DateInput):
    input_type = 'date'

# Create the form class.
class SetupForm(ModelForm):
    class Meta:
        model = Setup
        fields= (
            'stock_code','initial_transaction_date','playing_duration','principal',
            'transaction_cost_rate_buy','transaction_cost_rate_sell'
        )
        exclude = ('user',)
        # 新增 labels 對應
        labels = {
            'stock_code': '股票名稱',
            'initial_transaction_date': '交易起始日',
            'playing_duration': '遊玩天數',
            'principal': '本金',
            'transaction_cost_rate_buy': '交易成本比率(買進)',
            'transaction_cost_rate_sell': '交易成本比率(賣出)'
        }

        widgets = {
            'initial_transaction_date': DateInput(
                attrs = {'min': '2016-01-01', 'max': "2018-12-31"}),
            'principal': NumberInput(
                attrs = {'min': '0', 'max': '1000000', 'step': '10000', 'value': '100000', 'onkeydown':"return false"}),
        }

class AdviseSetupForm(ModelForm):
    principal = forms.IntegerField(label = '本金', 
					widget = forms.NumberInput(attrs={'id': 'id_principle', 'min': '10000', 'max': '1000000', 
					'step': '10000', 'value': '100000', 'onkeydown':"return false"}))
	
    initialStockHold = forms.IntegerField(label = '持有股數', 
					widget = forms.NumberInput(attrs={'id': 'id_initialStockHold', 'min': '100', 'max': '1000000', 
					'step': '100', 'value': '100', 'onkeydown':"return false", 'hidden': ''}))
    class Meta:
        model = AdviseSetup
        fields= ('stock_code', 'principal', 'initialStockHold')
        exclude = ('user',)
        # 新增 labels 對應 >> name
        labels = {
            'stock_code': '股票名稱',
            'principal': '本金',
            'initialStockHold': '持有股數'
        }

        widgets = {
            'principal': NumberInput(
                attrs={'id': 'id_principle', 'min': '0', 'max': '1000000', 'step': '10000', 
				'value': '100000', 'onkeydown':"return false", 'disabled': 'true'},),
			'initialStockHold': NumberInput(
                attrs={'id': 'id_initialStockHold', 'min': '0', 'max': '1000000', 'step': '10000', 
				'value': '0', 'onkeydown':"return false"}),
        }
		
        required = {
		    'true', 'false', 'true'
		}