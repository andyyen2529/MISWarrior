from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from TradingGame.models import User
from TradingGame.models import Stock

# ModelAdmin class
class UserAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'last_modify_date', 'created')

class StockAdmin(ImportExportModelAdmin):
	list_display = ('id', 'code', 'date', 'volumn', 'turnover', 'opening_price', 
		'high', 'low', 'closeing_price', 'spread', 'transaction_number')

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Stock, StockAdmin)