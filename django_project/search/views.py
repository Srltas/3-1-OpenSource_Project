from django.shortcuts import render
import urllib.request
import json

# Create your views here.
def index(request):
    # 입력 파라미터
    kw = request.GET.get('kw')
    page = int(request.GET.get('page', '1')) # 페이지

    if kw == '':
        page_list = {'error' : True}
    else:
        # 조회
        page_list = lib_search(kw, page)

    return render(request, 'search/search_result.html', page_list)

'''
도서 검색 함수

매개변수 :
title = 도서명
page = 요청 페이지

반환 리스트 :
'keyword' = 검색한 단어
'lastBuildDate' = 요청 날짜
'total' = 검색된 총 책 수
'number' = 현재 페이지 번호
'previousPageNumber' = 이전 페이지 번호
'nextPageNumber' = 다음 페이지 번호
'hasPrevious' = 이전 페이지 존재여부
'hasNext' = 다음 페이지 존재여부
'lastPage' = 총 페이지 수
'items' = 검색된 책의 리스트
'pageList' = 페이지 리스트


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
        curPage = '1000'
    else:
        curPage = str(page * 10 - 9)

    url = "https://openapi.naver.com/v1/search/book.json?query=" + encText + "&start=" + curPage  # json 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        json_data = json.loads(response_body.decode('utf-8'))
        # book_list = json_data["items"]
        # 책 리스트가 비어있으면 오류 반환
        if not json_data['items']:
            return {'error' : True}

        # isbn 13자리 주소만 남기기
        for item in json_data['items']:
            if item['isbn'] !='':
                item['isbn'] = item['isbn'].split(' ')[1]
            else:
                item['isbn'] = '0'

        # 검색한 단어 추가
        json_data['keyword'] = title

        # 이전 페이지 존재 여부, 다음 페이지 존재 여부 추가
        json_data['hasPrevious'] = True
        json_data['hasNext'] = True

        # 총 페이지 수 추가
        if json_data['total'] > 1000:
            json_data['lastPage'] = 100
        else:
            json_data['lastPage'] = int(json_data['total'] / 10 + 1)

        # 페이지 리스트 추가
        if page % 10 != 0:
            pageStart = page - (page % 10) + 1
            pageEnd = page - (page % 10) + 10
        else:
            pageStart = page - 9
            pageEnd = page
        if pageEnd < json_data['lastPage']:
            json_data['pageList'] = [i for i in range(pageStart, pageEnd+1)]
        else:
            json_data['pageList'] = [i for i in range(pageStart, json_data['lastPage']+1)]
            json_data['hasNext'] = False

        if pageStart == 1:
            json_data['hasPrevious'] = False

        # 다음 페이지 번호, 이전 페이지 번호 추가
        json_data['previousPageNumber'] = pageStart - 1
        json_data['nextPageNumber'] = pageEnd + 1

        # 현재페이지 번호 추가
        json_data['number'] = page

        #print(json_data)
        return json_data
    else:
        print("Error Code:" + rescode)
        return rescode