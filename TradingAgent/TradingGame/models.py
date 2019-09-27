from django.db import models
from django.contrib.auth.models import User

### 股票資料 ###
class Stock(models.Model):
	code = models.CharField(max_length = 30) # 股票代碼
	date = models.DateField() # 日期
	volumn = models.IntegerField() # 成交股數
	turnover = models.IntegerField() # 成交金額
	opening_price = models.FloatField() # 開盤價
	high = models.FloatField() # 最高價
	low = models.FloatField() # 最低價
	closing_price = models.FloatField() # 收盤價
	spread = models.FloatField() # 漲跌價差
	transaction_number = models.IntegerField() # 成交筆數

	class Meta:
		db_table = 'stock'

	def __str__(self):
		return '股票代碼：' + str(self.code) + '；日期：' + str(self.date)

### 交易歷史 ###
class History(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE) # 用戶編號(外來鍵)
	stock = models.ForeignKey(Stock, related_name = 'stocks', on_delete = models.CASCADE) # 股票資料編號(外來鍵)
	position_before_action = models.CharField(max_length = 1, choices = (('0', '現金'), ('1', '股票'))) # 行動之前的資產持有狀態
	rate_of_return_before_action = models.FloatField() # 行動之前的報酬率	
	action = models.CharField(max_length = 1, choices = (('0', '等待or持有'), ('1', '買or賣'))) # 行動

	class Meta:
		db_table = 'history'

### 交易設定 ###
class Setup(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE) # 用戶編號(外來鍵)
	stock_code = models.CharField(max_length = 4, choices = (('0050', '元大台灣50'), ('2430', '燦坤'))) # 股票代碼
	initial_transaction_date = models.DateField() # 起始交易日
	playing_duration = models.IntegerField() # 遊玩天數(只計股市交易日)
	principal = models.IntegerField() # 本金
	transaction_cost_rate = models.FloatField() # 交易成本比率

	class Meta:
		db_table = 'setup'