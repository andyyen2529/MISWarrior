from django.db import models
from django.contrib.auth.models import User

### 股票資料 ###
class Stock(models.Model):
	code = models.CharField(max_length = 30) # 股票代碼
	date = models.DateField() # 日期
	volumn = models.IntegerField() # 成交量(千股)
	turnover = models.IntegerField() # 成交值(千元)
	opening_price = models.FloatField() # 開盤價
	high = models.FloatField() # 最高價
	low = models.FloatField() # 最低價
	closing_price = models.FloatField() # 收盤價
	spread = models.FloatField() # 股價漲跌
	transaction_number = models.IntegerField() # 成交筆數

	class Meta:
		db_table = 'stock'

	def __str__(self):
		return '股票代碼：' + str(self.code) + '；日期：' + str(self.date)

### 股票代碼資料 ###
class StockCode(models.Model):
	code = models.CharField(max_length = 30) # 股票代碼

	class Meta:
		db_table = 'stockCode'

	def __str__(self):
		return str(self.code)

from datetime import datetime 
### 交易設定 ###
class Setup(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE) # 用戶編號(外來鍵)
	stock_code = models.ForeignKey(StockCode, on_delete = models.CASCADE) # 股票代碼
	initial_transaction_date = models.DateField() # 起始交易日
	playing_duration = models.IntegerField(choices = ((60, '60個交易日(三個月)'), (240, '240個交易日(一年)'))) 
		# 遊玩天數(只計股市交易日)
	principal = models.IntegerField() # 本金
	transaction_cost_rate = models.FloatField(choices = ((0.001425, '股票買賣現行手續費率(0.1425%)'), (0, '無'))) # 交易成本比率

	class Meta:
		db_table = 'setup'

	def __str__(self):
		return '使用者：' + str(self.user)

### 交易歷史 ###
class History(models.Model):
	setup = models.ForeignKey(Setup, on_delete = models.CASCADE) # 交易設定(外來鍵)
	day = models.IntegerField(default = 0) # 目前遊玩的天數
	action = models.CharField(max_length = 2, choices = (
		('等待', '等待'), ('持有', '持有'), ('買入', '買入'), ('賣出', '賣出'))
	) # 行動
	position_after_action = models.CharField(max_length = 1, choices = (('現金','現金'), ('股票','股票'))) # 行動之後的資產持有狀態
	last_trading_price_after_action = models.FloatField(null = True)  # 行動之後最後一筆的交易價格
	rate_of_return_after_action = models.FloatField() # 行動之後的報酬率	
	cash_held_after_action = models.FloatField(default = 0) # 行動之後持有的現金
	number_of_shares_held_after_action = models.FloatField(default = 0) # 行動之後持有的股數

	# 以下是電腦操作產生的交易歷史欄位
	action_robot = models.CharField(max_length = 2, choices = (
		('等待', '等待'), ('持有', '持有'), ('買入', '買入'), ('賣出', '賣出'))
	)
	position_after_action_robot = models.CharField(max_length = 1, choices = (('現金','現金'), ('股票','股票')))
	last_trading_price_after_action_robot = models.FloatField(null = True)
	rate_of_return_after_action_robot = models.FloatField()
	cash_held_after_action_robot = models.FloatField(default = 0)
	number_of_shares_held_after_action_robot = models.FloatField(default = 0)

	class Meta:
		db_table = 'history'

### 投資建議設定 ###		
class AdviseSetup(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE) # 用戶編號(外來鍵)
	stock_code = models.ForeignKey(StockCode, on_delete = models.CASCADE) # 股票代碼
	principal = models.IntegerField() # 本金
	initialStockHold = models.IntegerField() # 初始持有股數
	
### 排行榜歷史 ###
class RankingHistory(models.Model):
	setup = models.ForeignKey(Setup, on_delete = models.CASCADE) # 交易設定(外來鍵)
	final_rate_of_return = models.FloatField() # 最終報酬率
	
	class Meta:
		db_table = 'RankingHistory'
		#ordering = ['-final_rate_of_return']

	
