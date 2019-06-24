from django.db.models import Max, F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
from django.utils import timezone
from ipware.ip import get_ip

from board.models import Board, BoardStatus, HitCount
from user.models import User

pagesize = 10
pagersize = 5


def getlist(request):
    page = request.GET.get('page', '1')

    if int(page) < 1:
        return HttpResponseRedirect('/board')

    kwd = request.GET.get('kwd', '')
    title_filter = Q(title__icontains=kwd)
    status_filter = Q(status=BoardStatus.ACTIVE) if kwd != '' else Q()
    end_page = int((len(Board.objects.all().filter(title_filter & status_filter)) - 1) / pagesize) + 1

    if int(page) > end_page:
        return HttpResponseRedirect(f'/board/list?kwd={kwd}&page={end_page}')

    start_page = int((int(page) - 1) / pagersize) * pagersize
    start = (int(page) - 1) * pagesize
    boardlist = Board.objects.filter(title_filter & status_filter).order_by('-groupno', 'orderno')[start:start + pagesize]

    data = {'boardlist': boardlist,
            'kwd': kwd,
            'page': page,
            'pager': range(start_page + 1, start_page + 1 + pagersize),
            'start_page': start_page + 1,
            'end_page': end_page,
            'pagesize': pagesize,
            'pagersize': pagersize}

    return render(request, 'board/list.html', data)


def view(request, id=0):
    try:
        board = Board.objects.get(id=id)

        # 삭제된 게시글 열람 못함
        if board.status == BoardStatus.INACTIVE:
            return HttpResponseRedirect('/board')
    except Exception as e:
        return HttpResponseRedirect('/board')

    update_hit(request, board)

    # 글 목록으로 돌아가려고 할 때, 기존에 있던 페이지로 돌아가도록 함
    kwd = request.GET.get('kwd', '')
    page = request.GET.get('page', '')

    data = {'board': board, 'kwd': kwd, 'page': page}
    return render(request, 'board/view.html', data)


# 조회수 처리
def update_hit(request, board):
    ip = get_ip(request)

    try:
        hits = HitCount.objects.get(ip=ip, post=board)
    except Exception as e:      # 조회 기록이 없는 경우
        hits = HitCount(ip=ip, post=board)
        Board.objects.filter(id=board.id).update(hit=board.hit + 1)
        hits.save()
    else:                       # 조회 기록이 있으나 하루가 지난 경우
        if hits.date != timezone.now().date():
            Board.objects.filter(id=board.id).update(hit=board.hit + 1)
            hits.date = timezone.now()
            hits.save()


def write(request):
    if 'authuser' not in request.session:
        return HttpResponseRedirect('/board')

    data = {'groupno': (request.GET.get('groupno', '0')),
            'orderno': (request.GET.get('orderno', '0')),
            'depth': (request.GET.get('depth', '0')),
            'page': request.GET.get('page', '0'),
            'kwd': request.GET.get('kwd', '')}
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

    page = request.POST['page']
    kwd = request.POST['kwd']

    return HttpResponseRedirect(f'/board/list?page={page}&kwd={kwd}')


def modify(request, id=0):
    if 'authuser' not in request.session:
        return HttpResponseRedirect('/board')

    board = Board.objects.get(id=id)
    if board is None or board.user.id != request.session['authuser']['id']:
        return HttpResponseRedirect('/board')

    data = {'board': board,
            'page': request.GET.get('page', '0'),
            'kwd': request.GET.get('kwd', '')}
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

    page = request.POST['page']
    kwd = request.POST['kwd']

    return HttpResponseRedirect(f'/board/view/{boardid}?page={page}&kwd={kwd}')


def delete(request, id=0):
    if 'authuser' not in request.session:
        return HttpResponseRedirect('/board')

    board = Board.objects.get(id=id)

    if board is None or board.user.id != request.session['authuser']['id']:
        return HttpResponseRedirect('/board')

    # board.delete()
    board.status = BoardStatus.INACTIVE
    board.save()

    # 정상적인 경로로 삭제 시도 후 성공 시 원래 있었던 페이지로 redirect
    kwd = request.GET.get('kwd', '')
    page = request.GET.get('page', '')

    return HttpResponseRedirect(f'/board/list?page={page}&kwd={kwd}')
