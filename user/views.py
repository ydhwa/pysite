from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from user.models import User


def joinform(request):
    return render(request, 'user/joinform.html')


def joinsuccess(request):
    return render(request, 'user/joinsuccess.html')


def join(request):
    user = User()

    user.name = request.POST['name']
    user.email = request.POST['email']
    user.password = request.POST['password']
    user.gender = request.POST['gender']

    user.save()

    return HttpResponseRedirect('/user/joinsuccess')


def loginform(request):
    return render(request, 'user/loginform.html')


def login(request):
    results = User.objects.filter(email=request.POST['email']).filter(password=request.POST['password'])

    # 로그인 실패
    if len(results) == 0:
        return HttpResponseRedirect('user/loginform.html?result=fail')

    # 로그인 처리
    authuser = results[0]
    request.session['authuser'] = model_to_dict(authuser)

    return HttpResponseRedirect('/')


def logout(request):
    del request.session['authuser']

    return HttpResponseRedirect('/')


def updateform(request):
    user = User.objects.get(id=request.session['authuser']['id'])
    data = {
        'user': user
    }
    return render(request, 'user/updateform.html', data)


def update(request):
    user = User.objects.get(id=request.session['authuser']['id'])
    user.name = request.POST['name']
    user.gender = request.POST['gender']
    if not request.POST['password']:
        user.password = request.POST['password']
    user.save()

    # request.session['authuser'] = model_to_dict(user)
    request.session['authuser']['name'] = user.name

    return HttpResponseRedirect('user/updateform.html?result=success')
