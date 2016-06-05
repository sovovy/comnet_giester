from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from .models import Player
import datetime

def index(request):
	return render(request, 'game/index.html')

def init(request):
	nickname = request.POST['nick']
	players = Player.objects.all()
	count = players.count()
	players = players[count-1]
	if count>0:
		if players.pt =='':
			players.pt = nickname
			players.save()
			return HttpResponseRedirect('/chkDB')
	player = Player(po=nickname)
	player.save()
	return HttpResponseRedirect('/chkDB')

def chkDB(request): # 게임을 시작할 수 있는 지
   nickname = request.COOKIES['nick']
   pl = Player.objects.filter(po = nickname)
   pl2 = Player.objects.filter(pt = nickname)
   if pl2.exists():
      return HttpResponseRedirect('/set')
   if pl.exists():
      if pl[0].pt =='':
         return HttpResponseRedirect('/rfsh')
      else :
         return HttpResponseRedirect('/set')

def rfsh(request):
   nickname = request.COOKIES['nick']
   return render(request, 'game/rfsh.html')

def set(request):
	nickname = request.COOKIES['nick']
	## nickname 에 맞는 DB값 중 몇P인지 가져와서 쿠키에 저장 => whoami변수
	pl = Player.objects.filter(po = nickname)
	if pl.exists():
		whoami = "1P"
	else:
		whoami = "2P"

	context = { 'whoami' : whoami }
	return render(request, 'game/set.html', context)
	
def setChk(request):
	nickname = request.COOKIES['nick']
	hand = request.POST.get("hand") # 00001111 이런 포맷을 가지는 사용자의 패의 정보
	w = False #패가 정상적인지
	cnt=0
	for i in hand:
		if i == '1':
			cnt += 1
	if cnt==4:
		w = True

	pl = Player.objects.filter(po = nickname)
	pl2 = Player.objects.filter(pt = nickname)
	if w == True:
		if pl.exists():
			pl = pl[0]
			pl.board = pl.board[0:25] + hand[0:4] + pl.board[29:31] + hand[4:8] + pl.board[35:36]
			if pl.turn == "01":
				pl.turn = "11"
			else:
				pl.turn = "10"
			pl.save()

		elif pl2.exists():
			pl2 = pl2[0]
			pl2.board = pl2.board[0:1] + hand[4:8] + pl2.board[4:6] + hand[0:4] + pl2.board[11:36]
			if pl2.turn == "10":
				pl2.turn = "11"
			else:
				pl2.turn = "01"
			pl2.save()
		return HttpResponseRedirect('/wait')

	if pl.exists():
		whoami = "1P"
	elif pl2.exists():
		whoami = "2P"

	context = { 'whoami' : whoami }
	return render(request, 'game/set.html', context)

def wait(request):
	##if turn값의 1P이면 (게임 시작이 가능하면)
	# 	return HttpResponseRedirect('/game')c
	# else:
	return render(request, 'game/wait.html')

def game(request):
	#### 게임 내용들
	#	return render(request, 'game/game.html', context)

	# 임시 render
	li=[[9,4,4,4,4,8],[0,3,3,3,3,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,1,1,1,1,0],[9,2,2,2,2,8]]
	context = {'whoami':'1P','turn':'1P','board':li}
	return render(request, 'game/game.html',context)



def deal(request):
	nickname = request.COOKIES['nick']
	## nickname 에 맞는 DB값 중 몇P인지 가져와서 쿠키에 저장 => whoami변수

	x = request.POST.get("x")
	y = request.POST.get("y")
	vec = request.POST.get("vec")
	
	return render(request, 'game/wait.html')