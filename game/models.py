from django.db import models

class Player(models.Model):
	po = models.CharField(max_length=10, default='')
	pt = models.CharField(max_length=10, default='')
	turn = models.CharField(max_length=3, default='00')
	cont = models.TextField(default='044440\n033330\n000000\n000000\n011110\n022220')
	# 1-1P 파, 2-1P빨, 3-2P 파, 4-2P 빨