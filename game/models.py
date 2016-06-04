from django.db import models

class Player(models.Model):
	po = models.CharField(max_length=10, default='')
	pt = models.CharField(max_length=10, default='')
	turn = models.CharField(max_length=3, default='00')
	board = models.TextField(default='044440033330000000000000011110022220')
	# 1-1P 파, 2-1P빨, 3-2P 파, 4-2P 빨