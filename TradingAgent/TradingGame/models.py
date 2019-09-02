from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length = 30)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user"

class Stock(models.Model):
	code = models.CharField(max_length = 30) # 股票代碼
	date = models.DateField() # 日期
	volumn = models.IntegerField() # 成交股數
	turnover = models.IntegerField() # 成交金額
	opening_price = models.FloatField() # 開盤價
	high = models.FloatField() # 最高價
	low = models.FloatField() # 最低價
	closeing_price = models.FloatField() # 收盤價
	spread = models.FloatField() # 漲跌價差
	transaction_number = models.IntegerField() # 成交筆數

	class Meta:
		db_table = "stock"
