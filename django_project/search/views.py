from django.shortcuts import render
from django.core.paginator import Paginator
import urllib.request
import json

# Create your views here.
def index(request):
    kw = request.GET.get('kw', '')

    # 입력 파라미터
    page = request.GET.get('page', 1) # 페이지

    # 조회
    page_list = lib_search(kw, page)

    return render(request, 'search/search_result.html', page_list)


'''
도서 검색 함수

매개변수 :
title = 도서명
page = 요청 페이지

반환 리스트 :
'lastBuildDate' = 요청 날짜
'total' = 검색된 총 책 수
'lastPage' = 총 페이지 수
'items' = 검색된 책의 리스트

'items' 책의 속성 : 
'title' = 책 제목
'link' = 해당 책의 네이버 책 정보 url
'image' = 책의 표지 이미지 url
'author' = 저자
'price' = 가격
'discount' = 할인된 가격
'publisher' = 출판사
'pubdate' = 출판된 날짜
'isbn' = isbn
'description' = 책의 간력한 설명
'''
def lib_search(title, page=1):
    client_id = "NtvYyRB7KAzDG4v7Klbn"
    client_secret = "k2VLANkdJ_"
    encText = urllib.parse.quote(title)

    # 최대 100페이지 제한
    if page > 100:
        page = '1000'
    else:
        page = str(page * 10 - 9)

    url = "https://openapi.naver.com/v1/search/book.json?query=" + encText + "&start=" + page  # json 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        json_data = json.loads(response_body.decode('utf-8'))
        # book_list = json_data["items"]

        # 마지막 페이지 추가
        if json_data['total'] > 1000:
            json_data['lastPage'] = 100
        else:
            json_data['lastPage'] = int(json_data['total'] / 10 + 1)

        print(json_data)
        return json_data
    else:
        print("Error Code:" + rescode)
        return rescode