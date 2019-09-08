from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from TradingGame.models import User, Stock, History, Setup

# ModelAdmin class
class UserAdmin(ImportExportModelAdmin):
	list_display = ('id', 'name', 'last_modify_date', 'created')

class StockAdmin(ImportExportModelAdmin):
	list_display = ('id', 'code', 'date', 'volumn', 'turnover', 'opening_price', 
		'high', 'low', 'closeing_price', 'spread', 'transaction_number')

class HistoryAdmin(ImportExportModelAdmin):
	list_display = ('id', 'user', 'stock', 'position_before_action', 
		'rate_of_return_before_action', 'action')

class SetupAdmin(ImportExportModelAdmin):
	list_display = ('id', 'user', 'initial_transaction_date', 'playing_duration',
		'principal', 'transaction_cost_rate')

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(Setup, SetupAdmin)
