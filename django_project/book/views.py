from django.shortcuts import render
from users.models import ViewedBook
from django.utils import timezone
import urllib.request
import json
import numbers
import math

# Create your views here.


def bookDetail(request, book_id):
    # 검색한 책 DB에 추가
    if request.user.is_authenticated:
        lastBook = ViewedBook.objects.filter(user=request.user, book=book_id).order_by('-date').first()
        if lastBook is None or (timezone.now()-lastBook.date).days > 0 or (timezone.now()-lastBook.date).seconds > 1800:
            viewBook = ViewedBook(user=request.user, book=book_id)
            viewBook.save()

    # 매개변수 가져오기
    longitude = float(request.GET.get('longitude', -1))
    latitude = float(request.GET.get('latitude', -1))
    distance = int(request.GET.get('distance', 4))
    if distance > 10:
        distance = 10
    if distance < 2:
        distance = 2

    content = bookInfo(book_id)
    content['relatedBook'] = relatedBooks(book_id)
    if(longitude != -1):
        content['libs'] = searchLibraryWithBooks(book_id, longitude, latitude, distance=distance)
        content['range'] = distance

    print(content)
    return render(request, 'book/detail.html', content)

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

        return json_data
    else:
        print("Error Code:" + rescode)
        return rescode


"""
책을 소유한 도서관을 찾아서 리스트로 반환하는 함수

매개변수:
isbn = 검색할 책의 isbn
x = 사용자의 현재 위치의 위도
y = 사용자의 현재 위치의 경도
distance = 최대 탐색할 거리(km)

반환 리스트:
lib 도서관
    libCode 도서관코드
    libName 도서관명
    address 주소
    tel 전화번호
    fax FAX 번호
    latitude 위도
    longitude 경도
    homepage 홈페이지 URL
    closed 휴관일
    operatingTime 운영시간
    BookCount 단행본수
    distance 내 위치에서 도서관까지 거리(km)
    result 도서 소장여부('Y' or 'N')
"""
def searchLibraryWithBooks(isbn, x, y, distance=5):
    authKey = '1785223b91685a93407756245b23d0cea53ccfd7684fd72e6ac2da91d11b950c'
    encIsbn = str(isbn)

    # 도서관 목록 json 열기
    with open("./book/res/library.json", "r", encoding='utf-8') as st_json:
        jsonData = json.load(st_json)

    # 도서관 리스트에서 위도가 없는 도서관 삭제 후 각 도서관과의 거리 구하기
    jsonData = [lib for lib in jsonData['libs'] if 'latitude' in lib['lib'].keys()]
    for lib in jsonData:
        lib['lib']['distance'] = get_harversion_distance(x, y, float(lib['lib']['longitude']), float(lib['lib']['latitude']))

    # 도서관 리스트 거리순으로 정렬
    jsonData = sorted(jsonData, key=lambda x:x['lib']['distance'])

    # 내 위치에서 distance km 이내에 떨어진 도서관의 책 소유 여부 구한 후 리스트에 담아서 리턴
    libList = []
    for lib in jsonData:
        if lib['lib']['distance'] <= distance and len(libList) < 10:
            url = "http://data4library.kr/api/bookExist?format=json&authKey=" + authKey + "&isbn13=" + encIsbn + "&libCode=" + lib['lib']['libCode']
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            rescode = response.getcode()
            if (rescode == 200):
                response_body = response.read()
                libBookResult = json.loads(response_body.decode('utf-8'))
                libBookResult = libBookResult['response']

                print(libBookResult)
                lib['lib']['result'] = libBookResult['result']
                libList.append(lib)
        else:
            return libList

    return libList



'''
디그리를 라디안으로 변환
'''
def degree2radius(degree):
    return degree * (math.pi / 180)


'''
경위도 (x1,y1)과 (x2,y2) 점의 거리를 반환
Harversion Formula 이용하여 2개의 경위도간 거래를 구함(단위:Km)
'''
def get_harversion_distance(x1, y1, x2, y2, round_decimal_digits=2):
    if x1 is None or y1 is None or x2 is None or y2 is None:
        return None
    assert isinstance(x1, numbers.Number) and -180 <= x1 and x1 <= 180
    assert isinstance(y1, numbers.Number) and -90 <= y1 and y1 <= 90
    assert isinstance(x2, numbers.Number) and -180 <= x2 and x2 <= 180
    assert isinstance(y2, numbers.Number) and -90 <= y2 and y2 <= 90

    R = 6371  # 지구의 반경(단위: km)
    dLon = degree2radius(x2 - x1)
    dLat = degree2radius(y2 - y1)

    a = math.sin(dLat / 2) * math.sin(dLat / 2) \
        + (math.cos(degree2radius(y1)) \
           * math.cos(degree2radius(y2)) \
           * math.sin(dLon / 2) * math.sin(dLon / 2))
    b = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * b, round_decimal_digits)


"""
해당 창의 연관 도서 리스트 반환해주는 함수

매개변수:
isbn = 검색할 책의 isbn

반환 리스트:
resultNum 응답 결과 건수
docs 목록
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
"""
def relatedBooks(isbn):
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

        return json_data
    else:
        print("Error Code:" + rescode)
<<<<<<< HEAD
        return rescode
=======
        return rescode


>>>>>>> 581cf35ad1557d85c830f78fc31d82b294ed1e2b
