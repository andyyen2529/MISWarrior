from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from TradingGame.models import Stock, StockCode, History, Setup, AdviseSetup, RankingHistory

# ModelAdmin class
class StockAdmin(ImportExportModelAdmin):
	list_display = [f.name for f in Stock._meta.fields]

class StockCodeAdmin(ImportExportModelAdmin):
	list_display = ('id', 'code')

class HistoryAdmin(ImportExportModelAdmin):
	list_display = [f.name for f in History._meta.fields]

class SetupAdmin(ImportExportModelAdmin):
	list_display = [f.name for f in Setup._meta.fields]
		
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
