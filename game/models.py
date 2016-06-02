from django.db import models

class Player(models.Model):
	po = models.CharField(max_length=10, default='')
	pt = models.CharField(max_length=10, default='')
	turn = models.CharField(max_length=3, default='00')
	cont = models.TextField(default='033330\n044440\n000000\n000000\n011110\n022220')