from django.shortcuts import render, redirect
from .models import users
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.


def home(requset):
    user_id = requset.session.get('user')

    user_name = {}
    if user_id:
        user = users.objects.get(pk=user_id)
        user_name['name'] = '환영합니다 ' + user.username + '님'
        return render(requset, 'home/index.html',user_name)

    return render(requset, 'home/index.html')

def logout(request):
    if request.session.get('user'):
        del(request.session['user'])

    return redirect('/')

def login(request):
    if request.method == 'GET':
        return render(request, 'users/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)

        res_data = {}
        if not(username and password):
            res_data['error'] = '모든 값을 입력해야합니다.'
        else:
            user = users.objects.get(username=username)
            if check_password(password, user.password):
                # 비밀번호가 일치, 로그인 처리!
                request.session['user'] = user.id
                return redirect('/')
            else:
                res_data['error'] = '비밀번호를 틀렸습니다.'

        return render(request, 'users/login.html',res_data)

def signup(request):
    if request.method == 'GET':
        return render(request, 'users/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        useremail = request.POST.get('useremail',None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re-password', None)

        res_data = {}

        if not (username and useremail and password and re_password):
            res_data['error'] = '모든 문자를 입력해야합니다.'
        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다.'
        else:
            user = users(
                username=username,
                useremail=useremail,
                password=make_password(password)
            )

            user.save()

        return render(request, 'users/signup.html', res_data)