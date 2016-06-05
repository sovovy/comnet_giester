from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from .models import Player
import datetime

def index(request):
	return render(request, 'game/index.html')

def init(request):
	nickname = request.COOKIES['nick']

	pl = Player.objects.filter(po = nickname).exists()
	pl2 = Player.objects.filter(pt = nickname).exists()

	if pl or pl2:
		return render(request, 'game/index.html', {'overlap':'해당 닉네임은 중복됩니다.'})
		
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
	pl_hand = ""
	if w == True:
		if pl.exists():
			pl = pl[0]
			for i in range (0,8):
				if hand[i]=='0':
					pl_hand += '1'
				else:
					pl_hand += '2'
				pl.board = pl.board[:25] + pl_hand[:4] + pl.board[29:31] + pl_hand[4:] + pl.board[35]
			if pl.turn == "01":
				pl.turn = "1P"
				pl.save()
				return HttpResponseRedirect('/game')
			else:
				pl.turn = "10"
				pl.save()

		elif pl2.exists():
			pl2 = pl2[0]
			for i in range (0,8):
				if hand[i]=='0':
					pl_hand += '3'
				else:
					pl_hand += '4'
				pl2.board = pl2.board[0] + pl_hand[4:][::-1] + pl2.board[5:7] + pl_hand[:4][::-1] + pl2.board[11:]
			if pl2.turn == "10":
				pl2.turn = "1P"
				pl2.save()
				return HttpResponseRedirect('/game')
			else:
				pl2.turn = "01"
				pl2.save()
		return HttpResponseRedirect('/wait')

	else:
		return HttpResponseRedirect('/set')

def wait(request):
	nickname = request.COOKIES['nick']
	pl = Player.objects.filter(po = nickname)  # p1기준
	pl2 = Player.objects.filter(pt = nickname) # p2기준

	if pl.exists():
		if pl.turn == "11": 
			pl.turn = "1P"
			#whoami = "1P"
			pl.save()
			return HttpResponseRedirect('/game')
	elif pl2.exists():
		if pl2.turn =="11": 
			pl2.turn = "1P"
			#whoami = "2P"
			pl2.save()
			return HttpResponseRedirect('/game')
	# 둘다 셋팅 완료되었으면
	# 1P가 선을 잡도록 turn을 "1P"로 셋팅한 뒤
	# /game으로 redirect
	

	context = {'whoami' : whoami}
	return render(request, 'game/wait.html',context)
	# 아직 하나라도 셋팅되어있지 않다면 whoami정보 넘겨주며 wait.html render
	

def game(request):
	nickname = request.COOKIES['nick']
	pl = Player.objects.filter(po = nickname)  # p1기준
	pl2 = Player.objects.filter(pt = nickname) # p2기준

	if pl.exists(): # p1 기준
		whoami = '1P'
		if pl[0].board == "1PWIN":
			return HttpResponseRedirect('/win')
		elif pl[0].board == "2PWIN":
			return HttpResponseRedirect('/lose')
		else:
			li = pl[0].board
			turn = pl[0].turn
	elif pl2.exists(): # p2 기준
		whoami = '2P'
		if pl2[0].board == "2PWIN":
			return HttpResponseRedirect('/win')
		elif pl2[0].board == "1PWIN":
			return HttpResponseRedirect('/lose')
		else:
			li = pl2[0].board
			turn = pl2[0].turn
	# 승리가 결정난 경우 해당 페이지로 redirect
	# 그렇지 않은 경우에는 턴 데이터를 설정하고
	# 보드데이터를 읽어옴

	board =[li[0:5],
		li[6:11],
		li[12:17],
		li[18:23],
		li[24:29],
		li[30:35]]
	# 그 읽어온 보드데이터를 6개씩 끊어서 'board'를 구성하고 프론트에 전달

	context = {'whoami':whoami,'turn':turn,'board':board}
	return render(request, 'game/game.html',context)


	# 프론트에서 전송을 누르면 x,y,vec,whoami를 deal에게 post시킴

	
def win(request): #승리화면

	return render(request, 'game/win.html')#,context)

def lose(request): #패배화면	

	return render(request, 'game/lose.html')#,context)

	# 승부 결과 처리

def deal(request):
	nickname = request.COOKIES['nick']
	x = request.POST.get("x") -1
	y = request.POST.get("y") -1
	vec = request.POST.get("vec")

	pl = Player.objects.filter(po = nickname)
	pl2 = Player.objects.filter(pt = nickname)
	if pl.exists():
		board = pl[0].board
		whoami="1P"
	elif pl2.exists():
		board = pl2[0].board
		whoami="2P"

	li = []
	for i in range(0,6):
		li.append([])
		for j in range(0,6):
			li[i].append(board[i*6+j]) 	#board문자열을 리스트로 바꿔주기

	win1p=False
	win2p=False
	count1 =0
	count2 =0
	count3 =0
	count4 =0
	## board에서 상대방칸에 9,8 에 파란말 있고 플레이어 턴이면 승리
	
	## board 확인해서 1,2,3,4 숫자 카운트해서 승리판단 후 context 로 1pwin이나 2pwin 보냄
	for i in li:
		for j in i:
			if i==1:
				count1 +=1
			elif i==2:
				count2 +=1
			elif i==3:
				count3 +=1
			elif i==4:
				count4 +=1
	if count1 == 0:
		win2p=True
	if count2 == 0:
		win1p=True
	if count3 == 0:
		win1p=True
	if count4 == 0:
		win2p=True
	if li[0][0]==1 or li[0][5]==1:
		win1p=True
	if li[5][0]==3 or li[5][5]==3:
		win2p=True

	term=li[y][x]
	li[y][x]=0
	if vec == 0:
		li[y-1][x]=term
	if vec == 1:
		li[y][x+1]=term
	if vec == 2:
		li[y+1][x]=term
	if vec == 3:
		li[y][x-1]=term

	if win1p:
		li=[['1Pwin']]
	if win2p:
		li=[['2Pwin']]

	context = {'whoami':whoami,'board':li}
	## 승리 조건 ..
	## nickname 에 맞는 DB값 중 몇P인지 가져와서 쿠키에 저장 => whoami변수
	
	return render(request, 'game/game.html', context)