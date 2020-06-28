from django.shortcuts import render
from users.views import recommendedBooks


def index(request):
    content = {}
    if request.user.is_authenticated:
        content['rcmBooks'] = recommendedBooks(request.user)

    print(content)

    return render(request,'home/index.html', content)


# Create your views here.
