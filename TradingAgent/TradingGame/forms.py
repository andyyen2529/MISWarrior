from django.forms import ModelForm
from TradingGame.models import Setup

# Create the form class.
class SetupForm(ModelForm):
    class Meta:
        model = Setup
        fields= ('stock_code','initial_transaction_date','playing_duration','principal','transaction_cost_rate')
        exclude = ('user',)
        # 新增 labels 對應
        labels = {
            'stock_code': '股票名稱',
            'initial_transaction_date': '交易起始日',
            'playing_duration': '遊玩天數',
            'principal': '本金',
            'transaction_cost_rate': '交易成本比率'
        }