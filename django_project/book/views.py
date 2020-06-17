from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def bookDetail(request, book_id):
    return HttpResponse(book_id)