from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def bookDetail(request, book_id):
    return render(request, 'search/search_detail.html')