from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from TradingGame.models import Stock, StockCode, History, Setup, AdviseSetup, RankingHistory

# ModelAdmin class
class StockAdmin(ImportExportModelAdmin):
	list_display = ('id', 'code', 'date', 'volumn', 'turnover', 'opening_price', 
		'high', 'low', 'closing_price', 'spread', 'transaction_number')

class StockCodeAdmin(ImportExportModelAdmin):
	list_display = ('id', 'code', 'name')

class HistoryAdmin(ImportExportModelAdmin):
	list_display = ('id', 'setup', 'day', 
		#'position_before_action', 'last_trading_price_before_action',
		#'rate_of_return_before_action', 'cash_held_before_action', 'number_of_shares_held_before_action', 
		'action', 'position_after_action', 'last_trading_price_after_action', 'rate_of_return_after_action', 
		'cash_held_after_action', 'number_of_shares_held_after_action')

class SetupAdmin(ImportExportModelAdmin):
	list_display = ('id', 'stock_code', 'user', 'initial_transaction_date', 'playing_duration',
		'principal', 'transaction_cost_rate')
		
class AdviseSetupAdmin(ImportExportModelAdmin):
	list_display = ('id', 'stock_code', 'user', 'principal', 'initialStockHold')

class RankingHistoryAdmin(ImportExportModelAdmin):
	list_display = ('id', 'setup','final_rate_of_return')
	
# Register your models here.
admin.site.register(Stock, StockAdmin)
admin.site.register(StockCode, StockCodeAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(Setup, SetupAdmin)
admin.site.register(AdviseSetup, AdviseSetupAdmin)
admin.site.register(RankingHistory, RankingHistoryAdmin)
