from django.shortcuts import render
import urllib.request
import json

# Create your views here.


def bookDetail(request, book_id):
    content = bookInfo(book_id)

    return render(request, 'search/search_detail.html', content)


'''
책 정보 호출 함수

매개변수:
isbn = 검색할 책의 isbn

반환 리스트:
detail 상세
    book 도서
        no 순번
        bookname 도서명
        publication_date 출판일자
        authors 저자명
        publisher 출판사
        class_no 주제분류
        publication_year 출판년도
        bookImageURL 이미지 URL
        isbn ISBN
        isbn13 13자리 ISBN
        description 책소개
'''
def bookInfo(isbn):
    authKey = '1785223b91685a93407756245b23d0cea53ccfd7684fd72e6ac2da91d11b950c'
    encIsbn = str(isbn)

    url = "http://data4library.kr/api/srchDtlList?format=json&authKey=" + authKey + "&isbn13=" + encIsbn  # json 결과
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        json_data = json.loads(response_body.decode('utf-8'))
        json_data = json_data['response']

        print(json_data)
        return json_data
    else:
        print("Error Code:" + rescode)
        return rescode