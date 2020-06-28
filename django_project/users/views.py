
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from users.form import UserForm
from .models import ViewedBook
from django.utils import timezone
import urllib.request
import json
import random
# Create your views here.

def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'users/signup.html', {'form': form})



'''
개인의 도서 검색 기록을 기반으로 추천 도서 리스트 반환

매개변수:
user = 찾을 유저

반환 리스트:
book 도서
    no 순번
    bookname 도서명
    authors 저자명
    publisher 출판사
    publication_year 출판년도
    isbn13 13 자리 ISBN
    addition_symbol 부가기호
    vol 권
    class_no 주제분류
    bookImageURL 도서 이미지 URL
'''
def recommendedBooks(user):
    # 유저의 도서 검색기록 20개 가져오기
    viewBooks = ViewedBook.objects.filter(user=user).order_by('-date')
    if len(viewBooks) == 0:
        return []
    if len(viewBooks) > 20:
        viewBooks = viewBooks[:20]

    # 검색시간에 따라 가중치 설정
    weightDic = {}
    sumWieght = 0
    oldDays = (timezone.now()-viewBooks.reverse()[0].date).days
    for book in viewBooks:
        w = oldDays - (timezone.now()-book.date).days + 1
        sumWieght += w
        if book.book in weightDic:
            weightDic[book.book] += w
        else:
            weightDic[book.book] = w


    # 연관 도서 불러와서 가중치에 비례해서 책 리스트에 담기
    rcmBooks = []                           # 반한할 추천 도서 리스트
    maxBooks = 200                         # 리스트에 담을 최대 도서 수
    sumWieght = sum(weightDic.values())     # 가중치 함
    for isbn, w in weightDic.items():
        bookCount = int(maxBooks * (w/sumWieght))
        authKey = '1785223b91685a93407756245b23d0cea53ccfd7684fd72e6ac2da91d11b950c'
        encIsbn = str(isbn)
        url = "http://data4library.kr/api/recommandList?format=json&authKey=" + authKey + "&isbn13=" + encIsbn  # json 결과
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()

        if (rescode == 200):
            response_body = response.read()
            json_data = json.loads(response_body.decode('utf-8'))
            json_data = json_data['response']

            if json_data['resultNum'] == 0:
                continue

            if json_data['resultNum'] > bookCount:
                json_data['docs'] = json_data['docs'][:bookCount]

            rcmBooks.extend(json_data['docs'])

    # rcmBooks 섞기
    random.shuffle(rcmBooks)

    return rcmBooks

