from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
from guestbook.models import Guestbook


def getlist(request):
    guestbooklist = Guestbook.objects.all().order_by('-id')
    data = {'guestbooklist': guestbooklist}
    return render(request, 'guestbook/list.html', data)


def insert(request):
    guestbook = Guestbook()

    guestbook.name = request.POST['name']
    guestbook.password = request.POST['pass']
    guestbook.content = request.POST['content']

    guestbook.save()

    return HttpResponseRedirect('/guestbook')


def deleteform(request, id=0):
    if id == 0:
        return HttpResponseRedirect('/guestbook')

    data = {'id': id}
    return render(request, 'guestbook/deleteform.html', data)


def delete(request):
    guestbook = Guestbook.objects.filter(id=request.POST['id'], password=request.POST['password'])
    if guestbook is None:
        return HttpResponseRedirect('/guestbook')

    guestbook.delete()
    return HttpResponseRedirect('/guestbook')
