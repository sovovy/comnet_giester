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
			pl.s1 = '1'
			pl.save()

		elif pl2.exists():
			pl2 = pl2[0]
			for i in range (0,8):
				if hand[i]=='0':
					pl_hand += '3'
				else:
					pl_hand += '4'
			pl2.board = pl2.board[0] + pl_hand[4:][::-1] + pl2.board[5:7] + pl_hand[:4][::-1] + pl2.board[11:]
			pl2.s2 = '1'
			pl2.save()
		return HttpResponseRedirect('/wait')
	else:
		return HttpResponseRedirect('/set')

def wait(request):
	nickname = request.COOKIES['nick']
	pl = Player.objects.filter(po = nickname)  # p1기준
	pl2 = Player.objects.filter(pt = nickname) # p2기준

	if pl.exists():
		whoami = "1P"
		pl = pl[0]
		if pl.s1 =='1' and pl.s2 =='1':
			pl.turn = "1P"
			pl.save()
			return HttpResponseRedirect('/game')
	elif pl2.exists():
		whoami = "2P"
		pl2 = pl2[0]
		if pl2.s1 =='1' and pl2.s2 =='1':
			pl2.turn = "1P"
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
	whoami=''
	turn=''
	li=[]
	if pl.exists(): # p1 기준
		whoami = '1P'
		# 승리가 결정난 경우 winLose로 redirect
		if pl[0].board == "1Pwin" or pl[0].board == "2Pwin":
			return HttpResponseRedirect('/winLose')
		else:
		# 그렇지 않은 경우에는 턴 데이터를 설정하고
		# 보드데이터를 읽어옴
			board = pl[0].board
			turn = pl[0].turn
			for i in range(0,6):
				li.append([])
				for j in range(0,6):
					li[i].append(int(board[i*6+j]))
	elif pl2.exists(): # p2 기준
		whoami = '2P'
		# 승리가 결정난 경우 winLose로 redirect
		if pl2[0].board == "2Pwin" or pl2[0].board == "1Pwin":
			return HttpResponseRedirect('/winLose')
		else:
		# 그렇지 않은 경우에는 턴 데이터를 설정하고
		# 보드데이터를 읽어옴
			board = pl2[0].board[::-1]
			turn = pl2[0].turn
			for i in range(0,6):
				li.append([])
				for j in range(0,6):
					x = int(board[i*6+j])
					# 상대패는 뒤집고 보이는것도 다르게
					if(x == 8):
						li[i].append(9)
					elif(x == 9):
						li[i].append(8)
					elif(x == 1):
						li[i].append(3)
					elif(x == 2):
						li[i].append(4)
					elif(x == 3):
						li[i].append(1)
					elif(x == 4):
						li[i].append(2)
					else:
						li[i].append(x)

	# 먹은 패 개수 세기
	blueNum = 4
	redNum = 4
	for row in li:
		for x in row:	# 적의 패의 개수를 뺀다
			if x==3:
				blueNum-=1
			elif x==4:
				redNum-=1

	context = {'whoami':whoami,'turn':turn,'board':li, 'blueNum':range(blueNum), 'redNum':range(redNum)}
	return render(request, 'game/game.html',context)

def winLose(request): #승패결과처리
	nickname = request.COOKIES['nick']
	pl = Player.objects.filter(po = nickname) 
	pl2 = Player.objects.filter(pt = nickname)
	if pl.exists(): 
		whoami = "1P"
		if pl[0].board == "1Pwin":  #승리
			wl = "win"
		elif pl[0].board == "2Pwin": #패배
			wl = "lose"
	elif pl2.exists():
		whoami = "2P"
		if pl2[0].board == "2Pwin":  #승리
			wl = "win"
		elif pl2[0].board == "1Pwin": #패배
			wl = "lose"

	context = {'whoami' : whoami, 'winLose': wl}
	return render(request, 'game/winLose.html',context)

def deal(request):
	#game.html 으로부터 post받아옴
	nickname = request.COOKIES['nick']
	x = int(request.POST.get("xxx"))
	y = int(request.POST.get("yyy"))
	vec = int(request.POST.get("vec"))
	pl = Player.objects.filter(po = nickname)
	pl2 = Player.objects.filter(pt = nickname)
	win1p = False
	win2p = False
	turnagain = False

	# board 문자열을 리스트로 바꿔주기
	if pl.exists():
		user = pl[0]
		board = user.board
		whoami="1P"
	elif pl2.exists():
		user = pl2[0]
		board = user.board 
		whoami="2P"

	li = []
	for i in range(0,6):
		li.append([])
		for j in range(0,6):
			li[i].append(int(board[i*6+j]))

	# board에서 상대방 출구에 파란 말이면 승리판단
	
	if li[0][0]==1 or li[0][5]==1:
		win1p=True
		user.board="1Pwin"
		if user.turn=="1P":
			user.turn="2P"
		else:
			user.turn="1P"
		user.save()
		return HttpResponseRedirect('/game')
	if li[5][0]==3 or li[5][5]==3:
		win2p=True
		user.board="2Pwin"
		if user.turn=="1P":
			user.turn="2P"
		else:
			user.turn="1P"
		user.save()
		return HttpResponseRedirect('/game')

	# 패 이동
	if pl.exists():
		term=li[y][x]
		li[y][x]=0
		if vec == 0:
			if li[y-1][x]==1 or li[y-1][x]==2 or y-1<0:
				turnagain=True
				li[y][x]=term
			elif  y-1<0:
				turnagain=True
				li[y][x]=term
			else:
				li[y-1][x]=term
		if vec == 1:
			if li[y][x+1]==1 or li[y][x+1]==2 or x+1>5:
				turnagain=True
				li[y][x]=term
			elif x+1>5 :
				turnagain=True
				li[y][x]=term
			else:
				li[y][x+1]=term
		if vec == 2:
			if li[y+1][x]==1 or li[y+1][x]==2 or y+1>5:
				turnagain=True
				li[y][x]=term
			elif  y+1>5:
				turnagain=True
				li[y][x]=term
			else:
				li[y+1][x]=term
		if vec == 3:
			if li[y][x-1]==1 or li[y][x-1]==2 or x-1<0:
				turnagain=True
				li[y][x]=term
			elif  x-1<0:
				turnagain=True
				li[y][x]=term
			else:
				li[y][x-1]=term
	elif pl2.exists():
		x = 5 - x;	#2P기준으로 x,y값을 고치고 2P기준으로 말을 옮긴다.
		y = 5 - y;
		term=li[y][x]
		li[y][x]=0
		if vec == 0:
			if li[y+1][x]==3 or li[y+1][x]==4 or y+1>5:
				turnagain=True
				li[y][x]=term
			elif  y+1>5:
				turnagain=True
				li[y][x]=term
			else:
				li[y+1][x]=term
		if vec == 1:
			if li[y][x-1]==3 or li[y][x-1]==4 or x-1<0:
				turnagain=True
				li[y][x]=term
			elif  x-1<0:
				turnagain=True
				li[y][x]=term
			else:
				li[y][x-1]=term
		if vec == 2:
			if li[y-1][x]==3 or li[y-1][x]==4 or y-1<0:
				turnagain=True
				li[y][x]=term
			elif  y-1<0:
				turnagain=True
				li[y][x]=term
			else:
				li[y-1][x]=term
		if vec == 3:
			if li[y][x+1]==3 or li[y][x+1]==4 or x+1>5:
				turnagain=True
				li[y][x]=term
			elif  x+1>5:
				turnagain=True
				li[y][x]=term
			else:
				li[y][x+1]=term

	# board 확인해서 1,2,3,4 숫자 카운트해서 승리판단
	if not(win1p or win2p):
		count1 =0
		count2 =0
		count3 =0
		count4 =0
		for row in li:
			for x in row:
				if x==1:
					count1 +=1
				elif x==2:
					count2 +=1
				elif x==3:
					count3 +=1
				elif x==4:
					count4 +=1
		if count1 == 0:
			win2p=True
		if count2 == 0:
			win1p=True
		if count3 == 0:
			win1p=True
		if count4 == 0:
			win2p=True

	# 승리 판단
	if win1p:
		user.board="1Pwin"
	elif win2p:
		user.board="2Pwin"
	else:
		# li를 다시 문자열로 변경한 후 board 수정
		string=''
		for row in li:
			for x in row:
				string += str(x)
		user.board = string

	# turn 수정
	if turnagain:
		user.turn==user.turn
	else:
		if user.turn=="1P":
			user.turn="2P"
		else:
			user.turn="1P"
	user.save()

	return HttpResponseRedirect('/game')