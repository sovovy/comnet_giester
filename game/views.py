from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
	return render(request, 'game/index.html')

def init(request):
	nickname = request.POST.get("nick")
	## 닉네임 db에 알맞은 곳에 넣기
	return HttpResponseRedirect('/chkDB')

def chkDB(request): # 게임을 시작할 수 있는 지
	nickname = request.POST.get("nick")
	# 임시 render
	return HttpResponseRedirect('/rfsh')
	# if 이 닉네임이 있는 DB row에 1P 2P란이 둘다 차있으면:
	# 	return HttpResponseRedirect('/set')
	# else:

def rfsh(request):
	nickname = request.COOKIES['nickname']
	return render(request, 'game/rfsh.html')

def set(request):
	# nickname = request.COOKIES['nickname']
	## nickname 에 맞는 DB값 중 몇P인지 가져와서 쿠키에 저장 => whoami변수
	context = {'whoami':'1P'}
	return render(request, 'game/set.html', context)

def setChk(request):
	# 임시 render
	return render(request, 'game/set.html', context)

	# hand = request.POST.get("hand") # 00001111 이런 포맷을 가지는 사용자의 패의 정보
	
	## if hand에 0과 1의 비율이 안맞으면:
	# 	return HttpResponseRedirect('/set')
	# else:
	#   hand DB에 반영 (몇P인지 고려해서)
	#	DB에 turn값 알맞게 변경 => 둘다 완료되는 상태면 11이 아니라 1P로 update
	# 	return HttpResponseRedirect('/wait')

def game(request):
	#### 게임 내용들
	#	return render(request, 'game/game.html', context)

	# 임시 render
	return render(request, 'game/game.html')

def wait(request):
	##if turn값의 1P이면 (게임 시작이 가능하면)
	# 	return HttpResponseRedirect('/game')
	# else:
	return render(request, 'game/wait.html')