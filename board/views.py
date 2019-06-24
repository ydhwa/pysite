from django.db.models import Max, F
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
from board.models import Board, BoardStatus
from user.models import User

pagesize = 5


def getlist(request):
    page = request.GET.get('page', '1')

    if int(page) < 1:
        return HttpResponseRedirect('/board')

    kwd = request.GET.get('kwd', '')
    start_page = int((int(page) - 1) / pagesize) * pagesize
    start = (int(page) - 1) * pagesize
    boardlist = Board.objects.filter(title__icontains=kwd).order_by('-groupno', 'orderno')[start:start + pagesize]

    data = {'boardlist': boardlist,
            'kwd': kwd,
            'page': page,
            'pager': range(start_page + 1, start_page + 1 + pagesize),
            'start_page': start_page + 1,
            'end_page': int((len(Board.objects.all().filter(title__icontains=kwd)) - 1) / pagesize) + 1,
            'pagesize': pagesize}

    return render(request, 'board/list.html', data)


def view(request, id=0):
    if id == 0:
        return HttpResponseRedirect('/board')
    board = Board.objects.get(id=id)
    if board is None:
        return HttpResponseRedirect('/board')

    data = {'board': board}
    return render(request, 'board/view.html', data)


def write(request):
    if 'authuser' not in request.session:
        return HttpResponseRedirect('/board')

    data = {'groupno': ('0' if 'groupno' not in request.GET else request.GET['groupno']),
            'orderno': ('0' if 'orderno' not in request.GET else request.GET['orderno']),
            'depth': ('0' if 'depth' not in request.GET else request.GET['depth'])}
    return render(request, 'board/write.html', data)


def insert(request):
    if 'authuser' not in request.session:
        return HttpResponseRedirect('/board')

    board = Board()

    board.title = request.POST['title']
    board.content = request.POST['content']
    board.user = User(**request.session['authuser'])

    # 그룹번호 1부터 시작
    groupno = int(request.POST['groupno'])
    if groupno == 0:
        value = Board.objects.aggregate(max_groupno=Max('groupno'))
        groupno = 1 if value['max_groupno'] is None else value['max_groupno'] + 1
    board.groupno = groupno

    orderno = 0 if request.POST['groupno'] == '0' else int(request.POST['orderno'])
    Board.objects.filter(groupno=groupno).filter(orderno__gte=orderno + 1).update(orderno=F('orderno') + 1)
    board.orderno = orderno + 1

    board.depth = 0 if request.POST['groupno'] == '0' else int(request.POST['depth']) + 1

    board.save()

    return HttpResponseRedirect('/board')


def modify(request, id=0):
    if 'authuser' not in request.session:
        return HttpResponseRedirect('/board')

    board = Board.objects.get(id=id)
    if board is None or board.user.id != request.session['authuser']['id']:
        return HttpResponseRedirect('/board')

    data = {'board': board}
    return render(request, 'board/modify.html', data)


def update(request):
    if 'authuser' not in request.session:
        return HttpResponseRedirect('/board')

    boardid = int(request.POST['id'])
    board = Board.objects.get(id=boardid)

    if board is None or board.user.id != request.session['authuser']['id']:
        return HttpResponseRedirect('/board')

    board.title = request.POST['title']
    board.content = request.POST['content']

    board.save()

    return HttpResponseRedirect(f'/board/view/{boardid}')


def delete(request, id=0):
    if 'authuser' not in request.session:
        return HttpResponseRedirect('/board')

    board = Board.objects.get(id=id)

    if board is None or board.user.id != request.session['authuser']['id']:
        return HttpResponseRedirect('/board')

    # board.delete()
    board.status = BoardStatus.INACTIVE
    board.save()

    return HttpResponseRedirect('/board')
