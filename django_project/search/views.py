from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    kw = {} #임시로 값이 잘 들어갔나 확인용
    kw['kw'] = request.GET.get('kw', '')

    # 입력 파라미터
    page = request.GET.get('page', '1') # 페이지

    # 조회
    page_list = [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]

    # 페이징처리
    paginator = Paginator(page_list,10)
    page_obj = paginator.get_page(page)

    context = {'book_list': page_obj}
    return render(request, 'search/search_result.html', context)


