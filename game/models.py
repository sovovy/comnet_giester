from django.db import models

class Player(models.Model):
	po = models.CharField(max_length=10, default='')
	pt = models.CharField(max_length=10, default='')
	turn = models.CharField(max_length=3, default='00')
	 # 두가지정보를 가질수 있음
	 # 1. 셋팅관련
	 #   10 : 1p만 셋팅끝남, 01 : 2p만 셋팅 끝남
	 #   00 : 둘다 셋팅안함, 11 : 둘다 셋팅 끝남
	 # 2. 턴관련(게임 중)
	 #   1P : 1P 의 턴 , 2P : 2P의 턴
	board = models.TextField(default='944448033330000000000000011110922228')
	# 1-1P 파, 2-1P빨, 3-2P 파, 4-2P 빨