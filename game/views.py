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
	if Player.filter(pt = nickname).exist():
		return HttpResponseRedirect('/set')
	if Player.filter(po = nickname).exist():
		if pl.pt =='':
			return HttpResponseRedirect('/rfsh')
		else :
			return HttpResponseRedirect('/set')

	# 임시 render
	
	# if 이 닉네임이 있는 DB row에 1P 2P란이 둘다 차있으면:
	# 	return HttpResponseRedirect('/set')
	# else:

def rfsh(request):
	nickname = request.COOKIES['nick']
	return render(request, 'game/rfsh.html')

def set(request):
	nickname = request.COOKIES['nick']
	pl = Player.objects.filter(po = nickname)
	pl2 = Player.objects.filter(pt = nickname)
	if Player.filter(po = nickname).exist():
		T = pl[0].turn
		context = {'whoami':'1P','turn': T}
		return render(request, 'game/set.html', context)
	if Player.filter(pt = nickname).exist():
		T = pl2[0].turn
		context = {'whoami':'2P','turn': T}
		return render(request, 'game/set.html', context)

	## nickname 에 맞는 DB값 중 몇P인지 가져와서 쿠키에 저장 => whoami변수
def setChk(request):
	# 임시 render
	return render(request, 'game/set.html', context)

	# hand = request.POST.get("hand") # 00001111 이런 포맷을 가지는 사용자의 패의 정보
	
	#   hand DB에 반영 (몇P인지 고려해서)
	#	DB에 turn값 알맞게 변경 => 둘다 완료되는 상태면 11이 아니라 1P로 update
	# 	return HttpResponseRedirect('/wait')

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