from django.shortcuts import render

# Create your views here.
def index(request):
    kw = {} #임시로 값이 잘 들어갔나 확인용
    kw['kw'] = request.GET.get('kw', '')
    return render(request, 'search/search_result.html',kw)


